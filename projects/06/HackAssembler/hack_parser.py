import re
from main import InstructionTypes


class Parser:
    def __init__(self, asm: list):
        self.asm = asm
        self.cursor = 0
        self.last_instruction = None

    def has_more_instructions(self):
        return False if self.cursor >= len(self.asm) else True

    def _read(self):
        return self.asm[self.cursor]

    def read_and_move_cursor(self):
        self.last_instruction = self._read()
        self.cursor += 1
        return self.last_instruction

    def current_instruction_type(self):
        cur_inst = self._read()
        if "@" in cur_inst:
            return InstructionTypes.A.value
        elif "(" and ")" in cur_inst:
            return InstructionTypes.LABEL.value
        else:
            return InstructionTypes.C.value

    def parse(self):
        inst_map = {InstructionTypes.A.value: self.parse_a_instruction,
                    InstructionTypes.C.value: self.parse_c_instruction,
                    InstructionTypes.LABEL.value: self.parse_label_instruction}
        return inst_map[self.current_instruction_type()]()

    def parse_a_instruction(self):
        instruction = self.read_and_move_cursor()
        return instruction

    def parse_c_instruction(self):
        instruction = self.read_and_move_cursor()
        return instruction

    def parse_label_instruction(self):
        instruction = self.read_and_move_cursor()
        return instruction

