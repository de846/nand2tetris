from unittest import TestCase
from instruction_types import InstructionTypes
from tests.util import read_x_instructions
from tests.util import create_empty_parser, create_parser


INSTRUCTIONS = ["@1", "@2", "@10", "(LOOP)", "MD=A-1;JMP", "D", "0;JMP"]


class TestParser(TestCase):
    def test_has_no_more_instructions(self):
        parser = create_parser(INSTRUCTIONS)
        read_x_instructions(parser, len(INSTRUCTIONS))
        self.assertFalse(parser.has_more_instructions())

    def test_has_more_instructions(self):
        parser = create_parser(INSTRUCTIONS)
        parser.parse()
        self.assertTrue(parser.has_more_instructions())

    def test_get_a_instruction_type(self):
        parser = create_parser(INSTRUCTIONS)
        parser.read_and_move_cursor()
        instruction_type = parser.get_instruction_type()
        self.assertEqual(InstructionTypes.A.value, instruction_type)

    def test_get_c_instruction_type(self):
        parser = create_parser(INSTRUCTIONS)
        read_x_instructions(parser, 4)
        instruction_type = parser.get_instruction_type()
        self.assertEqual(InstructionTypes.C.value, instruction_type)

    def test_get_label_instruction_type(self):
        parser = create_parser(INSTRUCTIONS)
        read_x_instructions(parser, 3)
        instruction_type = parser.get_instruction_type()
        self.assertEqual(InstructionTypes.LABEL.value, instruction_type)

    def test_parse_a_instruction(self):
        parser = create_parser(INSTRUCTIONS)
        instruction = parser.parse()
        self.assertEqual((InstructionTypes.A.value, "1"), instruction)

    def test_parse_c_instruction_1(self):
        parser = create_parser(INSTRUCTIONS)
        instruction = read_x_instructions(parser, 5)
        self.assertEqual((InstructionTypes.C.value, ("MD", "A-1", "JMP")), instruction)

    def test_parse_c_instruction_2(self):
        parser = create_parser(INSTRUCTIONS)
        instruction = read_x_instructions(parser, 6)
        self.assertEqual((InstructionTypes.C.value, ("", "D", "")), instruction)

    def test_parse_c_instruction_3(self):
        parser = create_parser(INSTRUCTIONS)
        instruction = read_x_instructions(parser, 7)
        self.assertEqual((InstructionTypes.C.value, ("", "0", "JMP")), instruction)

    def test_parse_label_instruction(self):
        parser = create_parser(INSTRUCTIONS)
        instruction = read_x_instructions(parser, 4)
        self.assertEqual((InstructionTypes.LABEL.value, "LOOP"), instruction)

    def test_parse_label_instruction_explicit(self):
        parser = create_empty_parser()
        instruction = "(BAR)"
        out = parser.parse_label_instruction(instruction)
        self.assertEqual("BAR", out)

    def test_parse_a_instruction_explicit(self):
        parser = create_empty_parser()
        instruction = "@25477"
        out = parser.parse_a_instruction(instruction)
        self.assertEqual("25477", out)

    def test_parse_c_instruction_explicit(self):
        parser = create_empty_parser()
        instruction = "AM=M|D;JGT"
        out = parser.parse_c_instruction(instruction)
        self.assertEqual(("AM", "M|D", "JGT"), out)

    def test_label_parsing(self):
        parser = create_parser(INSTRUCTIONS)
        while parser.has_more_instructions():
            parser.parse()
