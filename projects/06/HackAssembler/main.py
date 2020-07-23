import logging

import click

from hack_parser import HackParser
from hack_symbol_table import HackSymbolTable
from hack_translator import HackTranslator

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@click.command()
@click.argument("asm", type=click.File("r"), required=True)
def main(asm):
    """
    The HackAssembler program to convert nand2tetris assembly to runnable
    machine code for the course's CPUEmulator.

    ASM is the file path to the source assembly file.
    """
    log.info("Reading source assembly into memory...")
    source = asm.read().splitlines()

    # Create a symbol table so it can be used in both the Parser and the Translator
    symbol_table = HackSymbolTable()
    parser = HackParser(source, symbol_table)
    translator = HackTranslator(symbol_table)
    parsed_code = parser.parse_source()
    log.debug(parsed_code)

    hack_filename = asm.name.replace(".asm", ".hack")
    log.info("Translating instructions...")
    with open(hack_filename, "w") as outfile:
        for code in parsed_code:
            translated_code = translator.translate(code)
            log.debug(f"CODE: {code}, \nBINARY: {translated_code}")
            outfile.write(translated_code + "\n")
    log.info(f"Machine code written to {hack_filename}.")


if __name__ == "__main__":
    main()
