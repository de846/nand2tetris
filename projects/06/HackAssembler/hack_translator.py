from instruction_types import InstructionTypes

COMP_MAP = {
    "0": ("101010", "0"),
    "1": ("111111", "0"),
    "-1": ("111010", "0"),
    "D": ("001100", "0"),
    "A": ("110000", "0"),
    "!D": ("001101", "0"),
    "!A": ("110001", "0"),
    "-D": ("001111", "0"),
    "-A": ("110011", "0"),
    "D+1": ("011111", "0"),
    "A+1": ("110111", "0"),
    "D-1": ("001110", "0"),
    "A-1": ("110010", "0"),
    "D+A": ("000010", "0"),
    "D-A": ("010011", "0"),
    "A-D": ("000111", "0"),
    "D&A": ("000000", "0"),
    "D|A": ("010101", "0"),
    "M": ("110000", "1"),
    "!M": ("110001", "1"),
    "-M": ("110011", "1"),
    "M+1": ("110111", "1"),
    "M-1": ("110010", "1"),
    "D+M": ("000010", "1"),
    "D-M": ("010011", "1"),
    "M-D": ("000111", "1"),
    "D&M": ("000000", "1"),
    "D|M": ("010101", "1"),
}

DEST_MAP = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
}

JUMP_MAP = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "010",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


class HackTranslator:
    @staticmethod
    def translate(instruction):
        instruction_type = instruction[0]
        types = {
            InstructionTypes.A.value: HackTranslator._translate_a,
            InstructionTypes.C.value: HackTranslator._translate_c,
            InstructionTypes.LABEL.value: HackTranslator._translate_label,
        }
        return types[instruction_type](instruction[1])

    @staticmethod
    def _translate_a(instruction):
        value = "0" + "{0:015b}".format(int(instruction))
        return value

    @staticmethod
    def _translate_c(instruction):
        dest, comp, jump = instruction
        value = (
            "111"
            + COMP_MAP[comp][1]
            + COMP_MAP[comp][0]
            + DEST_MAP[dest]
            + JUMP_MAP[jump]
        )
        return value

    @staticmethod
    def _translate_label(instruction):
        pass
