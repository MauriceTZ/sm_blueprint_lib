import shlex
from dataclasses import dataclass, field
from typing import Optional, Any
from src.sm_blueprint_lib import *


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
            token = token.rstrip(',')  # Strip trailing commas
            if not token:
                continue

            # Handle string literals
            if token.startswith('"') and token.endswith('"'):
                string_val = token[1:-1]
                if directive_name == ".asciiz":
                    # Explicitly append a null terminator for asciiz
                    string_val += "\0"
                args.append(string_val)
                continue

            # Handle numbers (Base 10 and Hex support via int(..., 0))
            try:
                args.append(int(token, 0))
            except ValueError:
                # If it's not a number, it's a register or label (e.g., r0, loop)
                args.append(token)

        return args

    def parse(self, code: str) -> dict[str, Segment]:
        lines = code.split('\n')
        pending_label = None

        for line_num, line in enumerate(lines, 1):
            clean_line = self._strip_comments(line)
            if not clean_line:
                continue

            # shlex with posix=False safely separates words while keeping "quoted strings" intact
            lexer = shlex.shlex(clean_line, posix=False)
            lexer.whitespace_split = True
            try:
                tokens = list(lexer)
            except ValueError as e:
                raise SyntaxError(
                    f"Line {line_num}: String literal formatting error. {e}")

            if not tokens:
                continue

            # 1. Handle Segment Changes
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

            statement = Statement(
                type='directive' if is_directive else 'instruction',
                name=command,
                args=self._parse_arguments(tokens[1:], command),
                label=pending_label
            )

            self.segments[self.current_segment_name].statements.append(
                statement)
            pending_label = None  # Reset label once it is attached to a statement

        return self.segments


assembly_code = """
# This is a comment
.segment rom # <-- diffent segments should be treated differently,
# I should be able to tell if a particular piece of code or data is in a particular segment.
data_array:
    .word 10, 30, 95, 100, 255, 0xEE2F
text_array: .asciiz "hello world!# this is still part of the string!!" # Here is the real comment. The string should have a null at the end.
.segment code
entry_point:
    ADD r0, r1, r3 # This is an inline comment
    SUB r1, r3, r1
loop:
    JUMP loop

"""

parser = AssemblyParser()
parsed_ast = parser.parse(assembly_code)

# Iterate through segments and print out the parsed structure
for segment_name, segment in parsed_ast.items():
    print(f"\n--- Segment: {segment_name.upper()} ---")
    for stmt in segment.statements:
        label_text = f"[{stmt.label}]" if stmt.label else ""
        print(f"{label_text:15} {stmt.type.upper():12} {stmt.name:8} args: {stmt.args}")


class Instruction:
    parts: list
    def connect(): ...


class ADD(Instruction):
    parts = ["or", *4*["and"], 6, *4*["and"]]

    def connect(parts_list: list[BaseLogicPart], reg_a, reg_b, reg_out):
        # Here should go this part of the old code, but now it should care
        # only on the connection aspect:

        # g = t.node("or", _to=reg_read(reg_a))
        # t.node(_to=reg_read(reg_b))
        # t.node(_to=adder_mode_select[3])
        # t.node(_to=reg_write(reg_adder_a))
        # t.node(_to=reg_write(reg_adder_b))
        # t.node(7, _to=adder_out_enable)
        # t.node()
        # t.node()
        # t.node(_to=reg_write(reg_out))
        # t.node()

        # Connect them in series
        # This should be slightly different in the jump cases.
        connect(parts_list, parts_list[1:])
        pass


class SUB(Instruction):
    parts = ["or", *4*["and"], 6, *4*["and"]]

    def connect(parts_list: list[BaseLogicPart], reg_a, reg_b, reg_out):
        # Same as in the ADD case:
        # t.node("or", _to=reg_read(reg_a))
        # t.node(_to=reg_read(reg_b))
        # t.node(_to=(adder_mode_select[3], adder_mode_select[2]))
        # t.node(_to=reg_write(reg_adder_a))
        # t.node(_to=reg_write(reg_adder_b))
        # t.node(7, _to=adder_out_enable)
        # t.node()
        # t.node()
        # t.node(_to=reg_write(reg_out))
        # t.node()

        connect(parts_list, parts_list[1:])
        pass


def create_instruction_parts(pos: Pos, parts_list: list):
    result = []
    for x, part in enumerate(parts_list):
        if isinstance(part, str):
            result.append(LogicGate(pos + (-x, 0, 0), "000000", part))
        elif isinstance(part, int):
            result.append(Timer(pos + (-x, 0, 0), "000000",
                          divmod(part, TICKS_PER_SECOND)))
    return result


code_initial_position = Pos(-2, 2, 0)
# First pass, create the necessary logic parts but dont do the connections yet.
for segment_name, segment in parsed_ast.items():
    if segment_name == "code":
        for z, stmt in enumerate(segment.statements):
            print(stmt)
            if stmt.type == "instruction":
                match stmt.name:
                    case "ADD":
                        stmt.parts = create_instruction_parts(
                            code_initial_position+Pos(0, 0, z), ADD.parts)
                    case "SUB":
                        stmt.parts = create_instruction_parts(
                            code_initial_position+Pos(0, 0, z), SUB.parts)

# Second pass, now we make the connections to other modules, also link instructions in series and do the jumps.
# I know this approach leaves the subroutines calls out because there is no way to know where to jump back from a
# subroutine. Maybe I could think of indexing the labels with a decoder and then pushing and pulling the return index into RAM.
# We are gonna focus on that later.
...