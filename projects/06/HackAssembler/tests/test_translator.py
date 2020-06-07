from unittest import TestCase
from tests.util import (
    read_x_instructions,
    create_parser_and_translator,
)


INSTRUCTIONS = ["@1", "@2", "@10", "(LOOP)", "MD=A-1;JMP", "D", "0;JMP"]


class TestTranslator(TestCase):
    def test_a_translation(self):
        parser, translator = create_parser_and_translator(INSTRUCTIONS)
        instruction = read_x_instructions(parser, 1)
        a_inst = translator.translate(instruction)
        self.assertEqual("0000000000000001", a_inst)

    def test_c_translation_1(self):
        parser, translator = create_parser_and_translator(INSTRUCTIONS)
        instruction = read_x_instructions(parser, 5)
        c_inst = translator.translate(instruction)
        self.assertEqual("1110110010011111", c_inst)

    def test_c_translation_2(self):
        parser, translator = create_parser_and_translator([])
        instruction = parser.parse("D")
        c_inst = translator.translate(instruction)
        self.assertEqual("1110001100000000", c_inst)

    def test_c_translation_3(self):
        parser, translator = create_parser_and_translator([])
        instruction = parser.parse("M=A")
        c_inst = translator.translate(instruction)
        self.assertEqual("1110110000001000", c_inst)

    def test_c_translation_4(self):
        parser, translator = create_parser_and_translator([])
        instruction = parser.parse("AM=D|M;JLE")
        c_inst = translator.translate(instruction)
        self.assertEqual("1111010101101110", c_inst)

    def test_a_variable(self):
        parser, translator = create_parser_and_translator([])
        instruction = parser.parse("@sum")
        inst = translator.translate(instruction)
        self.assertEqual("0000000000010000", inst)

        instruction = parser.parse("@i")
        inst = translator.translate(instruction)
        self.assertEqual("0000000000010001", inst)

        instruction = parser.parse("@sum")
        inst = translator.translate(instruction)
        self.assertEqual("0000000000010000", inst)
