from hack_parser import HackParser
from hack_symbol_table import HackSymbolTable
from hack_translator import HackTranslator


def read_x_instructions(parser, x):
    for _ in range(x - 1):
        parser.parse()
    return parser.parse()


def create_empty_parser():
    return HackParser([], HackSymbolTable())


def create_parser(asm: list):
    return HackParser(asm, HackSymbolTable())


def create_parser_and_translator(asm: list):
    table = HackSymbolTable()
    parser = HackParser(asm, table)
    translator = HackTranslator(table)
    return parser, translator
