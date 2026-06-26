import shlex
from dataclasses import dataclass, field
from typing import Optional, Any
from numpy import array
import numpy as np

# Assuming you are running this from outside the src directory, or adjust imports as needed
from src.sm_blueprint_lib.prebuilds.rom import rom
from src.sm_blueprint_lib.prebuilds.decoder import decoder
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
SCREEN_SIZE = 8, 8
PAGE_SIZE = ADDR_SIZE, 8

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
    label_index: Optional[int] = None
    instruction_index: Optional[int] = None
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
        self.labels: dict[str, Statement] = {}
        self.label_counter: int = 0
        self.instruction_counter: int = 0
        self.rom_data: list[int] = []

    def resolve_rom_data(self):
        """Pass to calculate ROM addresses and flatten data directives into a 1D array."""
        if "rom" not in self.segments:
            return

        # Pass 1: Assign addresses based on data lengths
        current_address = 0
        for stmt in self.segments["rom"].statements:
            if stmt.label:
                stmt.data_address = current_address

            if stmt.name == ".word":
                current_address += len(stmt.args)
            elif stmt.name == ".asciiz":
                current_address += len(stmt.args[0])

        # Pass 2: Extract data into the 1D rom_data array
        for stmt in self.segments["rom"].statements:
            if stmt.name == ".word":
                for arg in stmt.args:
                    if isinstance(arg, str) and arg in self.labels:
                        # Allow .word to store pointers to other labels!
                        target = self.labels[arg]
                        if target.data_address is not None:
                            self.rom_data.append(target.data_address)
                        elif target.instruction_index is not None:
                            self.rom_data.append(target.instruction_index)
                        else:
                            self.rom_data.append(0)
                    else:
                        self.rom_data.append(int(arg))
            elif stmt.name == ".asciiz":
                for char in stmt.args[0]:
                    self.rom_data.append(ord(char))

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

            # 2. Handle Labels
            if tokens[0].endswith(':'):
                pending_label = tokens[0][:-1]  # Strip the colon
                tokens = tokens[1:]             # Consume the token
                if not tokens:
                    continue  # Label was on a line by itself, move to next line

            # 3. Handle Directives and Instructions
            command = tokens[0]
            is_directive = command.startswith('.')

            current_instruction_index = None
            if not is_directive:
                current_instruction_index = self.instruction_counter
                self.instruction_counter += 1

            statement = Statement(
                type='directive' if is_directive else 'instruction',
                name=command,
                args=self._parse_arguments(tokens[1:], command),
                label=pending_label,
                label_index=self.label_counter if pending_label else None,
                instruction_index=current_instruction_index
            )

            if pending_label:
                self.labels[pending_label] = statement
                self.label_counter += 1

            self.segments[self.current_segment_name].statements.append(
                statement)
            pending_label = None  # Reset label once it is attached to a statement

        self.resolve_rom_data()
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
    def resolve_immediate(val, label_map):
        """If the immediate value is a label string, swap it out for its memory/instruction address."""
        if isinstance(val, str) and val in label_map:
            target = label_map[val]
            if target.data_address is not None:
                return target.data_address
            if target.instruction_index is not None:
                return target.instruction_index
        return val

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
        imm_val = Instruction.resolve_immediate(args[1], label_map)
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
        connect(parts_list[2], [hw_map["adder_mode_select"][3],
                                hw_map["adder_mode_select"][2]])
        connect(parts_list[3], hw_map["reg_write"](hw_map["reg_adder_a"]))
        connect(parts_list[4], hw_map["reg_write"](hw_map["reg_adder_b"]))
        connect(parts_list[5], hw_map["adder_out_enable"])
        connect(parts_list[8], hw_map["reg_write"](reg_out))

        connect(parts_list[:-1], parts_list[1:])


class SUBI(Instruction):
    parts = ["or", "and", "and", "and", "and", 6, "and", "and", "and", "and"]

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        reg_a = hw_map["get_reg"](args[0])
        imm_val = Instruction.resolve_immediate(args[1], label_map)
        reg_out = hw_map["get_reg"](args[2])

        connect(parts_list[0], hw_map["reg_read"](reg_a))
        connect(parts_list[1], [hw_map["adder_mode_select"][3],
                                hw_map["adder_mode_select"][2],
                                hw_map["mask"](hw_map["internal_bus"], imm_val)])
        connect(parts_list[2], hw_map["reg_write"](hw_map["reg_adder_b"]))
        connect(parts_list[3], hw_map["reg_write"](hw_map["reg_adder_a"]))
        connect(parts_list[5], hw_map["adder_out_enable"])
        connect(parts_list[8], hw_map["reg_write"](reg_out))

        connect(parts_list[:-1], parts_list[1:])


class SET(Instruction):
    parts = ["or", "and", "and"]

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        reg = hw_map["get_reg"](args[0])
        imm_val = Instruction.resolve_immediate(args[1], label_map)

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
    parts = ["or", "nand", "and", "and"]

    @staticmethod
    def get_fallthrough_part(parts_list):
        # The AND gate acts as the fallthrough trigger if Carry == 0
        return parts_list[2]

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        target_label = args[0]
        carry_flag = hw_map["carry_flag"]

        connect(parts_list[0], [parts_list[2], parts_list[3]])
        connect(carry_flag, [parts_list[1], parts_list[2]])
        connect(parts_list[1], parts_list[3])

        if target_label in label_map and label_map[target_label].parts:
            # AND triggers JUMP
            connect(parts_list[3], label_map[target_label].parts[0])


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
        addr_value = Instruction.resolve_immediate(args[1], label_map)

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
        addr_value = Instruction.resolve_immediate(args[1], label_map)

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


class CALL(Instruction):
    # Combines WRITERAM (5 ticks) + ADDI (10 ticks) sequentially. Total = 15 ticks.
    parts = ["or", "and", "and", "and", "and", "and",
             "and", "and", "and", "and", 6, "and", "and", "and", "and"]
    falls_through = False

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        target_label = args[0]
        current_idx = hw_map["current_stmt"].instruction_index
        return_idx = current_idx + 1
        r0 = hw_map["get_reg"]("r0")

        # --- 1. PUSH TO STACK (WRITERAM logic) ---
        # Tick 0: Push r0 to internal_bus (RAM Address)
        connect(parts_list[0], hw_map["reg_read"](r0))
        # Tick 1: Push return_idx to internal_bus
        connect(parts_list[1], hw_map["mask"](
            hw_map["internal_bus"], return_idx))
        # Tick 3: Trigger RAM Write Enable
        connect(parts_list[3], hw_map["ram_module"][5])

        # --- 2. INCREMENT STACK POINTER (ADDI r0, 1, r0 logic) ---
        # Tick 5: Read r0 to start ADDI
        connect(parts_list[5], hw_map["reg_read"](r0))
        # Tick 6: Adder Mode & Mask 1
        connect(parts_list[6], [hw_map["adder_mode_select"][3],
                                hw_map["mask"](hw_map["internal_bus"], 1)])
        # Tick 7: Write to adder B
        connect(parts_list[7], hw_map["reg_write"](hw_map["reg_adder_b"]))
        # Tick 8: Write to adder A
        connect(parts_list[8], hw_map["reg_write"](hw_map["reg_adder_a"]))
        # Tick 10: Adder Out Enable (after timer triggers)
        connect(parts_list[10], hw_map["adder_out_enable"])
        # Tick 13: Write back to r0
        connect(parts_list[13], hw_map["reg_write"](r0))

        # --- 3. JUMP ---
        # Tick 15: Jump to subroutine
        if target_label in label_map and label_map[target_label].parts:
            connect(parts_list[-1], label_map[target_label].parts[0])

        connect(parts_list[:-1], parts_list[1:])


class RET(Instruction):
    # Combines SUBI (10 ticks) + READRAM (10 ticks) sequentially. Total = 20 ticks.
    parts = ["or", "and", "and", "and", "and", 6, "and", "and", "and", "and",
             "and", "and", "and", "and", "and", "and", "and", "and", "and", "and"]
    falls_through = False

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        r0 = hw_map["get_reg"]("r0")

        # --- 1. DECREMENT STACK POINTER (SUBI r0, 1, r0 logic) ---
        # Tick 0: Read r0 to start SUBI
        connect(parts_list[0], hw_map["reg_read"](r0))
        # Tick 1: Adder Mode (SUB) & Mask 1
        connect(parts_list[1], [hw_map["adder_mode_select"][3],
                                hw_map["adder_mode_select"][2],
                                hw_map["mask"](hw_map["internal_bus"], 1)])
        # Tick 2: Write to adder B
        connect(parts_list[2], hw_map["reg_write"](hw_map["reg_adder_b"]))
        # Tick 3: Write to adder A
        connect(parts_list[3], hw_map["reg_write"](hw_map["reg_adder_a"]))
        # Tick 5: Adder Out Enable (after timer triggers)
        connect(parts_list[5], hw_map["adder_out_enable"])
        # Tick 8: Write back to r0
        connect(parts_list[8], hw_map["reg_write"](r0))

        # --- 2. POP FROM STACK (READRAM logic) ---
        # Tick 10: Push new r0 to internal_bus (RAM Address)
        connect(parts_list[10], hw_map["reg_read"](r0))
        # Tick 13: Trigger RAM Read Enable
        connect(parts_list[13], hw_map["ram_module"][8])

        # --- 3. TRIGGER RETURN DECODER ---
        # Tick 18: RAM has output value to internal_bus. Fire the decoder enable.
        if "return_decoder_enable" in hw_map:
            connect(parts_list[18], hw_map["return_decoder_enable"])

        connect(parts_list[:-1], parts_list[1:])


class READROM(Instruction):
    parts = ["or", "and", "and", "and", "and",
             "and", "and", "and", "and", "and", "and"]

    @staticmethod
    def connect(parts_list, args, hw_map, label_map):
        reg_data_in = hw_map["get_reg"](args[0])
        reg_addr = hw_map["get_reg"](args[1])

        connect(parts_list[0], hw_map["reg_read"](reg_addr))
        connect(parts_list[3], hw_map["rom_module"][6])  # Read Enable
        connect(parts_list[9], hw_map["reg_write"](reg_data_in))

        connect(parts_list[:-1], parts_list[1:])


INSTRUCTION_SET = {
    "ADD": ADD, "ADDI": ADDI,
    "SUB": SUB, "SUBI": SUBI,
    "SET": SET,
    "MOVE": MOVE,
    "JUMP": JUMP, "JC": JC,
    "WRITERAM": WRITERAM, "READRAM": READRAM,
    "WRITERAMA": WRITERAMA, "READRAMA": READRAMA,
    "WRITETRAM": WRITETRAM, "READTRAM": READTRAM,
    "PUTCHAR": PUTCHAR,
    "CALL": CALL, "RET": RET,
    "READROM": READROM,
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

    screen0 = timer_character_screen(bp, *SCREEN_SIZE, pos=(
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
.segment rom
    string0: .asciiz "Hi"
.segment code
entry_point:
    SET r0, 0   # Initialize stack pointer to 0

    SET r3, 0   # screen index
    loop:
        SET r1, string0 # pointer string position
        CALL print_string
        JUMP loop
    
print_string:
        READROM r2, r1  # Read from ROM at address in r1 into r2
        SUBI r2, 1, r4  # Subtract 1 from r2 and store in r4 (check for null terminator)
        JC print_string_end_loop
        PUTCHAR r2, r3   # Output character in r2 to screen at index in r3
        ADDI r1, 1, r1   # Increment ROM address in r1
        ADDI r3, 1, r3   # Increment screen index in r3
        JUMP print_string
    print_string_end_loop:
        RET
END_PROGRAM:
    """

    parser = AssemblyParser()
    parsed_ast = parser.parse(assembly_code)
    print(parser.rom_data)
    print(bytes(parser.rom_data))

    rom_module = rom(bp=bp, data=parser.rom_data,
                     page_size=PAGE_SIZE, pos=(-2-ADDR_SIZE, 30+PAGE_SIZE[1], 0))
    connect(internal_bus, np.append(rom_module[2], rom_module[4], axis=0))
    connect(rom_module[3], internal_bus)
    hw_map["rom_module"] = rom_module

    code_initial_position = Pos(-2, 2, 0)
    label_map = parser.labels
    # Here is where we will store the instruction indexers (AND gates) for the return decoder
    instruction_indexers = []
    instruction_indexers_input = None

    # --- C. Pass 1: Build the physical gates ---
    for segment_name, segment in parsed_ast.items():
        if segment_name == "code":
            for z, stmt in enumerate(segment.statements):
                if stmt.type == "instruction" and stmt.name in INSTRUCTION_SET:
                    InstructionClass = INSTRUCTION_SET[stmt.name]
                    stmt.parts = create_instruction_parts(
                        code_initial_position + Pos(0, 0, z), InstructionClass.parts)
                    instruction_indexers.append(g0 := LogicGate(code_initial_position + Pos(1, 0, 1+z),
                                                                "0000FF",
                                                                xaxis=-1, zaxis=-3))

    n_gates = get_bits_required(len(instruction_indexers))
    instruction_indexers_input = np.array([
        [LogicGate(code_initial_position + Pos(x-n_gates, -1, 0), "FF0000", "nor"),
         LogicGate(code_initial_position + Pos(x-n_gates, 0, 0), "FF0000", "or")]
        for x in range(n_gates)
    ], dtype=LogicGate)
    instruction_indexers_enable = LogicGate(
        code_initial_position + Pos(0, 0, 0), "FF0000", 1)
    connect(internal_bus, instruction_indexers_input)
    decoder(bp, len(instruction_indexers),
            precreated_inputs_binary=instruction_indexers_input,
            precreated_outputs=instruction_indexers,
            precreated_output_enable=instruction_indexers_enable)

    # --- EXPOSE INSTRUCTION DECODER ---
    # Inject the new decoder endpoints into the hardware map
    hw_map["return_decoder_outputs"] = instruction_indexers
    hw_map["return_decoder_enable"] = instruction_indexers_enable
    hw_map["return_decoder_input"] = instruction_indexers_input

    # --- D. Pass 2: Wire the Hardware and Link execution Flow ---
    for segment_name, segment in parsed_ast.items():
        if segment_name == "code":
            for i, stmt in enumerate(segment.statements):
                if stmt.type == "instruction" and stmt.name in INSTRUCTION_SET:
                    InstructionClass = INSTRUCTION_SET[stmt.name]

                    # Inject current statement into hardware map so instructions can access their own metadata
                    hw_map["current_stmt"] = stmt

                    # 1. Wire internal operation logic
                    InstructionClass.connect(
                        stmt.parts, stmt.args, hw_map, label_map)

                    # Wire the global Return Decoder so RET knows how to jump back here
                    if "return_decoder_outputs" in hw_map and stmt.instruction_index is not None:
                        connect(hw_map["return_decoder_outputs"]
                                [stmt.instruction_index], stmt.parts[0])

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
    bp.add(instruction_indexers, instruction_indexers_input,
           instruction_indexers_enable)

    save_blueprint("compiler output", bp)
    print("Compilation successful. Saved to blueprint.")
