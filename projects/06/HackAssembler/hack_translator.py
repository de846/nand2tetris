import logging

from hack_symbol_table import HackSymbolTable
from instruction_types import InstructionTypes

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Values taken from nand2tetris course slides
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
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


class HackTranslator:
    """The HackTranslator is responsible for translating parsed instructions based
    on the maps above, and for gets/sets to the symbol table."""

    def __init__(self, symbol_table: HackSymbolTable):
        self.symbol_table = symbol_table

        self.inst_map = {
            InstructionTypes.A.value: self._translate_a,
            InstructionTypes.C.value: self._translate_c,
            InstructionTypes.LABEL.value: self._translate_label,
        }

    def translate(self, instruction):
        """Main translate method which directs the instruction to a specific
        instruction translator based on its type."""
        instruction_type = instruction[0]
        return self.inst_map[instruction_type](instruction[1])

    def _translate_a(self, instruction):
        """Translate A instructions. If we can convert to int, we are dealing
        with a simple numerical address, otherwise we have a user-defined label
        and need to consult the symbol_table."""
        log.debug(f"Read instruction {instruction}")
        try:
            value = int(instruction)
        except ValueError:
            if not self.symbol_table.is_in_table(instruction):
                value = self.symbol_table.add(instruction)
                log.debug(f"Adding {instruction} at address {value}")
            else:
                value = self.symbol_table.get(instruction)
                log.debug(f"Retrieved {instruction} at address {value}")
                # value = self.symbol_table.get(instruction)
        value = "0" + "{0:015b}".format(int(value))
        return value

    def _translate_c(self, instruction):
        dest, comp, jump = instruction
        value = (
            "111"
            + COMP_MAP[comp][1]
            + COMP_MAP[comp][0]
            + DEST_MAP[dest]
            + JUMP_MAP[jump]
        )
        return value

    def _translate_label(self, instruction):
        """Do nothing at this stage when encountering a label."""
        pass
