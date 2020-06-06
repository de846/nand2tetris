from unittest import TestCase
from hack_translator import HackTranslator
from hack_parser import HackParser
from main import InstructionTypes
from tests.util import read_x_instructions


INSTRUCTIONS = ["@1", "@2", "@10", "(LOOP)", "MD=A-1;JMP", "D", "0;JMP"]


class TestTranslator(TestCase):
    def test_a_translation(self):
        parser = HackParser(INSTRUCTIONS)
        instruction = read_x_instructions(parser, 1)
        translator = HackTranslator()
        a_inst = translator.translate(instruction)
        self.assertEqual("0000000000000001", a_inst)

    def test_c_translation(self):
        parser = HackParser(INSTRUCTIONS)
        instruction = read_x_instructions(parser, 5)
        translator = HackTranslator()
        c_inst = translator.translate(instruction)
        self.assertEqual("1110110010011111", c_inst)
