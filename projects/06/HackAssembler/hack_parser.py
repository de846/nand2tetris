import re
from instruction_types import InstructionTypes
from hack_symbol_table import HackSymbolTable
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class HackParser:
    def __init__(self, asm: list, symbol_table: HackSymbolTable):
        self.asm = asm
        self.cursor = 0
        self.symbol_table = symbol_table
        self.rom_address = 0

    def has_more_instructions(self):
        return False if self.cursor >= len(self.asm) else True

    def _read(self):
        return self.asm[self.cursor].strip()

    def read_and_move_cursor(self):
        instruction = self.filter_instruction(self._read())
        self.cursor += 1
        return instruction

    def filter_instruction(self, instruction):
        comments = instruction.find("//")
        if comments != -1:
            instruction = instruction[:comments].strip()
        return instruction if instruction else None

    def get_instruction_type(self, instruction=None):
        cur_inst = instruction or self.filter_instruction(self._read())

        if not cur_inst:
            return InstructionTypes.IGNORE.value
        elif "@" in cur_inst:
            return InstructionTypes.A.value
        elif "(" and ")" in cur_inst:
            return InstructionTypes.LABEL.value
        else:
            return InstructionTypes.C.value

    def parse(self, instruction=None):
        inst_map = {
            InstructionTypes.A.value: self.parse_a_instruction,
            InstructionTypes.C.value: self.parse_c_instruction,
            InstructionTypes.LABEL.value: self.parse_label_instruction,
            InstructionTypes.IGNORE.value: self.ignore_instruction,
        }
        cur_type = self.get_instruction_type(instruction)
        return cur_type, inst_map[cur_type](instruction)

    def ignore_instruction(self, _=None):
        self.cursor += 1
        return None

    def parse_a_instruction(self, instruction=None):
        instruction = instruction or self.read_and_move_cursor()
        inst = instruction[1:]
        self.rom_address += 1
        return inst

    def parse_c_instruction(self, instruction=None):
        instruction = instruction or self.read_and_move_cursor()
        out = re.search("([AMD]*=|^)(.*?)(?=(;[A-Z]*|$))", instruction)
        dest = out.group(1)
        if dest:
            dest = dest.strip("=")
        comp = out.group(2)
        jump = out.group(3)
        if jump:
            jump = jump.strip(";")
        self.rom_address += 1
        return dest, comp, jump

    def parse_label_instruction(self, instruction=None):
        instruction = instruction or self.read_and_move_cursor()
        match = re.match(r"\((.+)\)", instruction)
        label_name = match.group(1)
        log.debug(f"{label_name} points to {self.rom_address}")
        self.symbol_table.add(label_name, str(self.rom_address))
        return label_name

    def parse_source(self):
        parsed_code = []
        while self.has_more_instructions():
            code = self.parse()
            if (
                code
                and code[0] is not InstructionTypes.IGNORE.value
                and code[0] is not InstructionTypes.LABEL.value
            ):
                parsed_code.append(code)
        return parsed_code
