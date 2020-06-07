import click
from hack_parser import HackParser
from hack_translator import HackTranslator
from hack_symbol_table import HackSymbolTable
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@click.command()
@click.argument("asm", type=click.File("r"), required=True)
def main(asm):
    log.info("Reading source assembly into memory...")
    source = asm.read()

    symbol_table = HackSymbolTable()
    translator = HackTranslator(symbol_table)
    parser = HackParser(source.splitlines(), symbol_table)
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
