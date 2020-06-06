from unittest import TestCase
from hack_parser import HackParser
from instruction_types import InstructionTypes
from tests.util import read_x_instructions

INSTRUCTIONS = ["@1", "@2", "@10", "(LOOP)", "MD=A-1;JMP", "D", "0;JMP"]


class TestParser(TestCase):
    def test_has_no_more_instructions(self):
        parser = HackParser(INSTRUCTIONS)
        read_x_instructions(parser, len(INSTRUCTIONS))
        self.assertFalse(parser.has_more_instructions())

    def test_has_more_instructions(self):
        parser = HackParser(INSTRUCTIONS)
        parser.read_and_move_cursor()
        self.assertTrue(parser.has_more_instructions())

    def test_get_a_instruction_type(self):
        parser = HackParser(INSTRUCTIONS)
        parser.read_and_move_cursor()
        instruction_type = parser.current_instruction_type()
        self.assertEqual(InstructionTypes.A.value, instruction_type)

    def test_get_c_instruction_type(self):
        parser = HackParser(INSTRUCTIONS)
        read_x_instructions(parser, 4)
        instruction_type = parser.current_instruction_type()
        self.assertEqual(InstructionTypes.C.value, instruction_type)

    def test_get_label_instruction_type(self):
        parser = HackParser(INSTRUCTIONS)
        read_x_instructions(parser, 3)
        instruction_type = parser.current_instruction_type()
        self.assertEqual(InstructionTypes.LABEL.value, instruction_type)

    def test_parse_a_instruction(self):
        parser = HackParser(INSTRUCTIONS)
        instruction = parser.parse()
        self.assertEqual((InstructionTypes.A.value, "1"), instruction)

    def test_parse_c_instruction_1(self):
        parser = HackParser(INSTRUCTIONS)
        instruction = read_x_instructions(parser, 5)
        self.assertEqual((InstructionTypes.C.value, ("MD", "A-1", "JMP")), instruction)

    def test_parse_c_instruction_2(self):
        parser = HackParser(INSTRUCTIONS)
        instruction = read_x_instructions(parser, 6)
        self.assertEqual((InstructionTypes.C.value, ("", "D", "")), instruction)

    def test_parse_c_instruction_3(self):
        parser = HackParser(INSTRUCTIONS)
        instruction = read_x_instructions(parser, 7)
        self.assertEqual((InstructionTypes.C.value, ("", "0", "JMP")), instruction)

    def test_parse_label_instruction(self):
        parser = HackParser(INSTRUCTIONS)
        instruction = read_x_instructions(parser, 4)
        self.assertEqual((InstructionTypes.LABEL.value, "LOOP"), instruction)
