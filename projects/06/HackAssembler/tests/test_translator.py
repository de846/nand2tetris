from unittest import TestCase
from hack_translator import HackTranslator
from hack_parser import Parser
from main import InstructionTypes

INSTRUCTIONS = ["@1", "@2", "@10", "(LOOP)", "MD=A-1;JMP", "D", "0;JMP"]


class TestTranslator(TestCase):
    def test_a_translation(self):
        parser = Parser(INSTRUCTIONS)
        instruction = parser.parse()
        translator = HackTranslator()
        a_inst = translator.translate(instruction)
        self.assertEqual(a_inst, "0000000000000001")

    def test_c_translation(self):
        parser = Parser(INSTRUCTIONS)
        parser.parse()
        parser.parse()
        parser.parse()
        parser.parse()
        instruction = parser.parse()
        translator = HackTranslator()
        c_inst = translator.translate(instruction)
        self.assertEqual(c_inst, "1110110010011111")

