import re
from main import InstructionTypes


class HackParser:
    def __init__(self, asm: list):
        self.asm = asm
        self.cursor = 0

    def has_more_instructions(self):
        return False if self.cursor >= len(self.asm) else True

    def _read(self):
        return self.asm[self.cursor]

    def read_and_move_cursor(self):
        instruction = self._read()
        self.cursor += 1
        return instruction

    def current_instruction_type(self):
        cur_inst = self._read()
        if "@" in cur_inst:
            return InstructionTypes.A.value
        elif "(" and ")" in cur_inst:
            return InstructionTypes.LABEL.value
        else:
            return InstructionTypes.C.value

    def parse(self):
        inst_map = {
            InstructionTypes.A.value: self.parse_a_instruction,
            InstructionTypes.C.value: self.parse_c_instruction,
            InstructionTypes.LABEL.value: self.parse_label_instruction,
        }
        cur_type = self.current_instruction_type()
        return cur_type, inst_map[cur_type]()

    def parse_a_instruction(self):
        instruction = self.read_and_move_cursor()
        inst = instruction[1:]
        return inst

    def parse_c_instruction(self):
        instruction = self.read_and_move_cursor()
        out = re.search("([AMD]*=|^)(.*?)(?=(;[A-Z]*|$))", instruction)
        dest = out.group(1)
        if dest:
            dest = dest.strip("=")
        comp = out.group(2)
        jump = out.group(3)
        if jump:
            jump = jump.strip(";")
        return dest, comp, jump

    def parse_label_instruction(self):
        instruction = self.read_and_move_cursor()
        match = re.match(r"(\()([A-Za-z]+)(\))", instruction)
        return match.group(2)
