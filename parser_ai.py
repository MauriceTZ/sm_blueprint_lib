import shlex
from dataclasses import dataclass, field
from typing import Optional, Any
from numpy import array
import numpy as np

# Assuming you are running this from outside the src directory, or adjust imports as needed
from src.sm_blueprint_lib.constants import TICKS_PER_SECOND
from src.sm_blueprint_lib import Blueprint, LogicGate, Timer, Pos, check_pos
from src.sm_blueprint_lib.utils import connect, get_bits_required, num_to_bit_list, save_blueprint
from src.sm_blueprint_lib.prebuilds.adder import cla_1tick
from src.sm_blueprint_lib.prebuilds.register import register, counter_register
from src.sm_blueprint_lib.prebuilds.ram import ram
from src.sm_blueprint_lib.prebuilds.timer_ram_multiclient import timer_ram_multiclient
from src.sm_blueprint_lib.prebuilds.screens.timer_character_screen import timer_character_screen


ADDR_SIZE = 8
START_ADDR = 0x1000
NUM_REGISTERS = 8
NUM_ADDR_TIMER_RAM = 64

# ==============================================================================
# 1. AST AND PARSER DEFINITIONS
# ==============================================================================


@dataclass
class Statement:
    """Base representation of a parsed line of code."""
    type: str  # 'instruction' or 'directive'
    name: str  # The opcode (ADD) or directive (.word)
    args: list[Any]
    label: Optional[str] = None
    parts: list[Any] = field(default_factory=list)


@dataclass
class Segment:
    """Represents a section of memory/code (e.g., rom, code)."""
    name: str
    statements: list[Statement] = field(default_factory=list)


class AssemblyParser:
    def __init__(self):
        self.segments: dict[str, Segment] = {}
        self.current_segment_name: str = "default"
        self.segments[self.current_segment_name] = Segment(
            self.current_segment_name)

    def _strip_comments(self, line: str) -> str:
        """Safely removes comments, ignoring '#' characters inside quoted strings."""
        in_string = False
        for i, char in enumerate(line):
            if char == '"':
                in_string = not in_string
            elif char == '#' and not in_string:
                return line[:i].strip()
        return line.strip()

    def _parse_arguments(self, tokens: list[str], directive_name: str) -> list[Any]:
        """Parses arguments into integers, strings, or keeps them as register labels."""
        args = []
        for token in tokens:
            token = token.rstrip(',')
            if not token:
                continue

            if token.startswith('"') and token.endswith('"'):
                string_val = token[1:-1]
                if directive_name == ".asciiz":
                    string_val += "\0"
                args.append(string_val)
                continue

            try:
                args.append(int(token, 0))
            except ValueError:
                args.append(token)

        return args

    def parse(self, code: str) -> dict[str, Segment]:
        lines = code.split('\n')
        pending_label = None

        for line_num, line in enumerate(lines, 1):
            clean_line = self._strip_comments(line)
            if not clean_line:
                continue

            lexer = shlex.shlex(clean_line, posix=False)
            lexer.whitespace_split = True
            try:
                tokens = list(lexer)
            except ValueError as e:
                raise SyntaxError(
                    f"Line {line_num}: String literal formatting error. {e}")

            if not tokens:
                continue

            if tokens[0] == '.segment':
                if len(tokens) < 2:
                    raise SyntaxError(
                        f"Line {line_num}: .segment requires a name.")
                self.current_segment_name = tokens[1]
                if self.current_segment_name not in self.segments:
                    self.segments[self.current_segment_name] = Segment(
                        self.current_segment_name)
                continue

            if tokens[0].endswith(':'):
                pending_label = tokens[0][:-1]
                tokens = tokens[1:]
                if not tokens:
                    continue

            command = tokens[0]
            is_directive = command.startswith('.')

            statement = Statement(
                type='directive' if is_directive else 'instruction',
                name=command,
                args=self._parse_arguments(tokens[1:], command),
                label=pending_label
            )

            self.segments[self.current_segment_name].statements.append(
                statement)
            pending_label = None

        return self.segments


# ==============================================================================
# 2. INSTRUCTION SET ARCHITECTURE
# ==============================================================================

class Instruction:
    parts: list = []
    falls_through: bool = True

    @staticmethod
    def get_fallthrough_part(parts_list):
        """Returns the part that should connect to the next instruction."""
        return parts_list[-1]

    @staticmethod
    def connect(parts_list: list, args: list, hw_map: dict, label_map: dict):
        pass


class ADD(Instruction):
    parts = ["or", "and", "and", "and", "and", 7, "and", "and", "and", "and"]

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        reg_a = hw_map["get_reg"](args[0])
        reg_b = hw_map["get_reg"](args[1])
        reg_out = hw_map["get_reg"](args[2])

        connect(parts_list[0], hw_map["reg_read"](reg_a))
        connect(parts_list[1], hw_map["reg_read"](reg_b))
        connect(parts_list[2], hw_map["adder_mode_select"][3])
        connect(parts_list[3], hw_map["reg_write"](hw_map["reg_adder_a"]))
        connect(parts_list[4], hw_map["reg_write"](hw_map["reg_adder_b"]))
        connect(parts_list[5], hw_map["adder_out_enable"])
        connect(parts_list[8], hw_map["reg_write"](reg_out))

        connect(parts_list[:-1], parts_list[1:])


class ADDI(Instruction):
    parts = ["or", "and", "and", "and", "and", 6, "and", "and", "and", "and"]

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        reg_a = hw_map["get_reg"](args[0])
        imm_val = args[1]
        reg_out = hw_map["get_reg"](args[2])

        connect(parts_list[0], hw_map["reg_read"](reg_a))
        connect(parts_list[1], [hw_map["adder_mode_select"][3],
                hw_map["mask"](hw_map["internal_bus"], imm_val)])
        connect(parts_list[2], hw_map["reg_write"](hw_map["reg_adder_b"]))
        connect(parts_list[3], hw_map["reg_write"](hw_map["reg_adder_a"]))
        connect(parts_list[5], hw_map["adder_out_enable"])
        connect(parts_list[8], hw_map["reg_write"](reg_out))

        connect(parts_list[:-1], parts_list[1:])


class SUB(Instruction):
    parts = ["or", "and", "and", "and", "and", 7, "and", "and", "and", "and"]

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        reg_a = hw_map["get_reg"](args[0])
        reg_b = hw_map["get_reg"](args[1])
        reg_out = hw_map["get_reg"](args[2])

        connect(parts_list[0], hw_map["reg_read"](reg_a))
        connect(parts_list[1], hw_map["reg_read"](reg_b))
        connect(parts_list[2], [hw_map["adder_mode_select"]
                [3], hw_map["adder_mode_select"][2]])
        connect(parts_list[3], hw_map["reg_write"](hw_map["reg_adder_a"]))
        connect(parts_list[4], hw_map["reg_write"](hw_map["reg_adder_b"]))
        connect(parts_list[5], hw_map["adder_out_enable"])
        connect(parts_list[8], hw_map["reg_write"](reg_out))

        connect(parts_list[:-1], parts_list[1:])


class SET(Instruction):
    parts = ["or", "and", "and"]

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        reg = hw_map["get_reg"](args[0])
        imm_val = args[1]

        connect(parts_list[0], hw_map["mask"](hw_map["internal_bus"], imm_val))
        connect(parts_list[1], hw_map["reg_write"](reg))

        connect(parts_list[:-1], parts_list[1:])


class MOVE(Instruction):
    parts = ["or", "and", "and", "and", "and"]

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        reg_from = hw_map["get_reg"](args[0])
        reg_to = hw_map["get_reg"](args[1])

        connect(parts_list[0], hw_map["reg_read"](reg_from))
        connect(parts_list[3], hw_map["reg_write"](reg_to))

        connect(parts_list[:-1], parts_list[1:])


class JUMP(Instruction):
    parts = ["or"]
    falls_through = False  # Terminate thread flow naturally

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        target_label = args[0]
        if target_label in label_map and label_map[target_label].parts:
            connect(parts_list[0], label_map[target_label].parts[0])


class JC(Instruction):
    parts = ["or", "nand", "and"]

    @staticmethod
    def get_fallthrough_part(parts_list):
        # The NAND gate acts as the fallthrough trigger if Carry == 0
        return parts_list[1]

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        target_label = args[0]
        carry_flag = hw_map["carry_flag"]

        connect(parts_list[0], [parts_list[1], parts_list[2]])
        connect(carry_flag, [parts_list[1], parts_list[2]])

        if target_label in label_map and label_map[target_label].parts:
            # AND triggers JUMP
            connect(parts_list[2], label_map[target_label].parts[0])


class WRITERAM(Instruction):
    parts = ["or", "and", "and", "and", "and", "and"]

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        reg_data_out = hw_map["get_reg"](args[0])
        reg_addr = hw_map["get_reg"](args[1])

        connect(parts_list[0], hw_map["reg_read"](reg_data_out))
        connect(parts_list[1], hw_map["reg_read"](reg_addr))
        connect(parts_list[4], hw_map["ram_module"][5])  # Write Enable

        connect(parts_list[:-1], parts_list[1:])


class READRAM(Instruction):
    parts = ["or", "and", "and", "and", "and",
             "and", "and", "and", "and", "and"]

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        reg_data_in = hw_map["get_reg"](args[0])
        reg_addr = hw_map["get_reg"](args[1])

        connect(parts_list[0], hw_map["reg_read"](reg_addr))
        connect(parts_list[3], hw_map["ram_module"][8])  # Read Enable
        connect(parts_list[8], hw_map["reg_write"](reg_data_in))

        connect(parts_list[:-1], parts_list[1:])


class WRITERAMA(Instruction):
    parts = ["or", "and", "and", "and", "and", "and"]

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        reg_data_out = hw_map["get_reg"](args[0])
        addr_value = args[1]

        connect(parts_list[0], hw_map["reg_read"](reg_data_out))
        connect(parts_list[3], hw_map["mask"](
            hw_map["internal_bus"], addr_value))
        connect(parts_list[4], hw_map["ram_module"][5])  # Write Enable

        connect(parts_list[:-1], parts_list[1:])


class READRAMA(Instruction):
    parts = ["or", "and", "and", "and", "and", "and", "and", "and"]

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        reg_data_in = hw_map["get_reg"](args[0])
        addr_value = args[1]

        connect(parts_list[0], hw_map["mask"](
            hw_map["internal_bus"], addr_value))
        connect(parts_list[1], hw_map["ram_module"][8])  # Read Enable
        connect(parts_list[6], hw_map["reg_write"](reg_data_in))

        connect(parts_list[:-1], parts_list[1:])


class WRITETRAM(Instruction):
    parts = ["or", "and", "and", "and", "and", "xor", "and", "and"]

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        reg_data_out = hw_map["get_reg"](args[0])
        reg_addr = hw_map["get_reg"](args[1])

        connect(parts_list[0], hw_map["reg_read"](reg_data_out))
        connect(parts_list[1], hw_map["reg_read"](reg_addr))
        connect(parts_list[3], hw_map["timer_ram_module"]
                [3][0][7][1])  # timer ram data register
        connect(parts_list[4], (hw_map["timer_ram_module"][3][0][8][1],  # timer ram address register
                                # mode selector register
                                hw_map["timer_ram_module"][3][0][9][1],
                                # write mode
                                hw_map["timer_ram_module"][3][0][9][0][1, 2]))
        # Selfwired xor gate to wait for timer ram operation to finish (wait bit)
        connect(parts_list[5], parts_list[5])
        # Operation complete.
        connect(hw_map["timer_ram_module"][3][0][11], parts_list[6])
        connect(parts_list[7], parts_list[5])  # Clear wait bit

        connect(parts_list[:-1], parts_list[1:])


class READTRAM(Instruction):
    parts = ["or", "and", "and", "and", "xor",
             "and", "and", "and", "and", "and"]

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        reg_data_in = hw_map["get_reg"](args[0])
        reg_addr = hw_map["get_reg"](args[1])

        connect(parts_list[0], hw_map["reg_read"](reg_addr))
        connect(parts_list[3], (hw_map["timer_ram_module"][3][0][8][1],  # timer ram address register
                                # mode selector register
                                hw_map["timer_ram_module"][3][0][9][1],
                                # read mode
                                hw_map["timer_ram_module"][3][0][9][0][[0, 1], 2]))
        # Selfwired xor gate to wait for timer ram operation to finish (wait bit)
        connect(parts_list[4], parts_list[4])
        # Operation complete.
        connect(hw_map["timer_ram_module"][3][0][11], parts_list[5])
        connect(parts_list[6], parts_list[4])  # Clear wait bit
        connect(parts_list[5], hw_map["timer_ram_module"]
                [3][0][13])    # timer ram data register out
        connect(parts_list[8], hw_map["reg_write"](reg_data_in))

        connect(parts_list[:-1], parts_list[1:])


class PUTCHAR(Instruction):
    parts = ["or", "and", "and", "and", "and", "and", "xor", "and", "and"]

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        reg_char = hw_map["get_reg"](args[0])
        reg_char_index = hw_map["get_reg"](args[1])

        connect(parts_list[0], hw_map["reg_read"](reg_char))
        connect(parts_list[1], hw_map["reg_read"](reg_char_index))
        connect(parts_list[4], hw_map["screen0"][5][3][0][8][1])
        connect(parts_list[5], (hw_map["screen0"][5][3][0][7][1],
                                # mode selector register
                                hw_map["screen0"][5][3][0][9][1],
                                # write mode
                                hw_map["screen0"][5][3][0][9][0][1, 2]))
        # Selfwired xor gate to wait for screen operation to finish (wait bit)
        connect(parts_list[6], parts_list[6])
        # Operation complete.
        connect(hw_map["screen0"][5][3][0][11], parts_list[7])
        connect(parts_list[8], parts_list[6])  # Clear wait bit

        connect(parts_list[:-1], parts_list[1:])


INSTRUCTION_SET = {
    "ADD": ADD, "ADDI": ADDI,
    "SUB": SUB, "SET": SET,
    "MOVE": MOVE, "JUMP": JUMP,
    "JC": JC,
    "WRITERAM": WRITERAM, "READRAM": READRAM,
    "WRITERAMA": WRITERAMA, "READRAMA": READRAMA,
    "WRITETRAM": WRITETRAM, "READTRAM": READTRAM,
    "PUTCHAR": PUTCHAR,
}


# ==============================================================================
# 3. CPU BUILDER & COMPILER EXECUTION
# ==============================================================================

def create_instruction_parts(pos: Pos, parts_list: list):
    result = []
    # Using Z-axis offset for each part within an instruction layout
    for x, part in enumerate(parts_list):
        if isinstance(part, str):
            result.append(LogicGate(pos + (-x, 0, 0),
                          "000000", part, xaxis=3, zaxis=-1))
        elif isinstance(part, int):
            result.append(Timer(pos + (-x, 0, 0), "000000",
                          divmod(part - 1, TICKS_PER_SECOND), xaxis=3, zaxis=-1))
    return result


if __name__ == "__main__":
    bp = Blueprint()

    # --- A. Setup Core CPU Architecture (From old_code.py) ---
    def mask(array_bus, mask_val: int, bit_length=ADDR_SIZE):
        """Returns the specific logic gates from the bus that should be lit for the value"""
        return array_bus[num_to_bit_list(mask_val, bit_length)]

    internal_bus = array([LogicGate((x, 0, 0), "FF00FF", 1)
                         for x in range(ADDR_SIZE)], dtype=LogicGate)

    PC = counter_register(
        bp, ADDR_SIZE, with_decrement=False, pos=(2+ADDR_SIZE, 2, 0))

    def reg_write(reg): return reg[1]
    def reg_read(reg): return reg[2]
    def reg_din(reg): return reg[0][:, -1]
    def reg_dout(reg): return reg[0][:, 0]

    PC_write = reg_write(PC[0])
    PC_read = reg_read(PC[0])

    connect(internal_bus, reg_din(PC[0]))
    connect(reg_dout(PC[0]), internal_bus)

    registers = [register(bp, ADDR_SIZE, pos=(2+ADDR_SIZE, 10+5*y, 0))
                 for y in range(NUM_REGISTERS)]
    for r in registers:
        connect(reg_dout(r), internal_bus)
        connect(internal_bus, reg_din(r))

    adder_subtractor = cla_1tick(bp, ADDR_SIZE, (-3-2*ADDR_SIZE, 10, 0))
    reg_adder_a = register(bp, ADDR_SIZE, OE=False, pos=(-2-ADDR_SIZE, 12, 2))
    reg_adder_b = register(bp, ADDR_SIZE, OE=False, pos=(-2-ADDR_SIZE, 12, 0))

    adder_out = adder_subtractor[8]  # enable_a4 (output array)
    adder_out_enable = adder_subtractor[10]  # enable_out global
    carry_flag = adder_subtractor[6][-1]  # or_b3[-1]

    adder_mode_select = [
        LogicGate((-4-ADDR_SIZE, 12, 0), "0000FF", 2),
        LogicGate((-4-ADDR_SIZE, 13, 0), "000000", 0),
        LogicGate((-4-ADDR_SIZE, 14, 0), "FF0000", 2),
        LogicGate((-5-ADDR_SIZE, 13, 0), "FF0000", 1)
    ]
    adder_mode_select[2].connect(adder_mode_select[1]).connect(
        adder_mode_select[0]).connect(adder_mode_select[0]).connect(adder_mode_select[2])
    adder_mode_select[3].connect(adder_mode_select[1])
    # add_subtract global flag
    adder_mode_select[0].connect(adder_subtractor[9])

    connect(reg_dout(reg_adder_a), adder_subtractor[0])
    connect(reg_dout(reg_adder_b), adder_subtractor[1])
    connect(internal_bus, reg_din(reg_adder_a))
    connect(internal_bus, reg_din(reg_adder_b))
    connect(adder_out, internal_bus)

    ram_module = ram(bp, ADDR_SIZE, 8, (-2-ADDR_SIZE, 26, 2))
    ram_din = [LogicGate((-2-ADDR_SIZE+x, 27, 0), "FF0000", 1)
               for x in range(ADDR_SIZE)]
    connect(internal_bus, ram_din)
    connect(ram_din, ram_module[1])
    connect(ram_module[2], internal_bus)
    connect(internal_bus, ram_module[3])
    connect(internal_bus, ram_module[6])

    timer_ram_module = timer_ram_multiclient(bp,
                                             bit_length=ADDR_SIZE,
                                             num_address=NUM_ADDR_TIMER_RAM,
                                             num_clients=1,
                                             pos=(-5-get_bits_required(NUM_ADDR_TIMER_RAM)-ADDR_SIZE, 17, 0))
    connect(internal_bus, timer_ram_module[3][0][7][0][:, 3])
    connect(internal_bus, timer_ram_module[3][0][8][0][:, 2])
    connect(timer_ram_module[3][0][12], internal_bus)

    screen0 = timer_character_screen(bp, 16, 4, pos=(
        0, -20, 0), do_preview=False, monitor_ghosting=2)
    connect(internal_bus, screen0[3])
    # timer screen address register
    connect(internal_bus, screen0[5][3][0][8][0][:, 2])

    # Ensure HW dependencies are bound for the compiler
    hw_map = {
        "get_reg": lambda r_str: registers[int(r_str.replace('r', ''))],
        "reg_read": reg_read,
        "reg_write": reg_write,
        "mask": mask,
        "internal_bus": internal_bus,
        "reg_adder_a": reg_adder_a,
        "reg_adder_b": reg_adder_b,
        "adder_mode_select": adder_mode_select,
        "adder_out_enable": adder_out_enable,
        "carry_flag": carry_flag,
        "ram_module": ram_module,
        "timer_ram_module": timer_ram_module,
        "screen0": screen0,
    }

    # --- B. Run the Parser ---
    assembly_code = """
    
    .segment code
    entry_point:
        SET r0, 32
        SET r1, 0
    loop:
        PUTCHAR r0, r1
        ADDI r1, 1, r1
        ADDI r0, 1, r0
        JUMP loop
        # WRITETRAM r0, r0
        # READTRAM r2, r0
        # ADDI r0, 1, r0
        # JUMP loop
    """

    parser = AssemblyParser()
    parsed_ast = parser.parse(assembly_code)
    code_initial_position = Pos(-2, 2, 0)
    label_map = {}

    # --- C. Pass 1: Build the physical gates and index the labels ---
    for segment_name, segment in parsed_ast.items():
        if segment_name == "code":
            for z, stmt in enumerate(segment.statements):
                if stmt.label:
                    label_map[stmt.label] = stmt
                if stmt.type == "instruction" and stmt.name in INSTRUCTION_SET:
                    InstructionClass = INSTRUCTION_SET[stmt.name]
                    stmt.parts = create_instruction_parts(
                        code_initial_position + Pos(0, 0, z), InstructionClass.parts)

    # --- D. Pass 2: Wire the Hardware and Link execution Flow ---
    for segment_name, segment in parsed_ast.items():
        if segment_name == "code":
            for i, stmt in enumerate(segment.statements):
                if stmt.type == "instruction" and stmt.name in INSTRUCTION_SET:
                    InstructionClass = INSTRUCTION_SET[stmt.name]

                    # 1. Wire internal operation logic
                    InstructionClass.connect(
                        stmt.parts, stmt.args, hw_map, label_map)

                    # 2. Wire execution flow to NEXT instruction
                    if InstructionClass.falls_through:
                        if i + 1 < len(segment.statements):
                            next_stmt = segment.statements[i + 1]
                            if next_stmt.parts:
                                flow_out = InstructionClass.get_fallthrough_part(
                                    stmt.parts)
                                connect(flow_out, next_stmt.parts[0])

    # --- E. FINALIZE: Add everything to the Blueprint ---
    all_generated_instruction_parts = []
    for segment_name, segment in parsed_ast.items():
        for stmt in segment.statements:
            if stmt.parts:
                all_generated_instruction_parts.append(stmt.parts)

    # Add core CPU modules
    bp.add(internal_bus, adder_mode_select, ram_din)

    # Add compiled instructions
    bp.add(*all_generated_instruction_parts)

    save_blueprint("compiler output", bp)
    print("Compilation successful. Saved to blueprint.")
