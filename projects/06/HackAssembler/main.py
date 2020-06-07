import click
from hack_parser import HackParser
from hack_translator import HackTranslator
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@click.command()
@click.argument("asm", type=click.File("r"), required=True)
def main(asm):
    log.info("Reading source assembly into memory...")
    source = asm.read()
    log.info("Parsing assembly code...")
    parser = HackParser(source.splitlines())
    parsed_code = parser.parse_source()
    log.debug(parsed_code)
    hack_filename = asm.name.replace(".asm", ".hack")
    with open(hack_filename, "w") as outfile:
        for code in parsed_code:
            outfile.write(HackTranslator.translate(code) + "\n")


if __name__ == "__main__":
    main()
