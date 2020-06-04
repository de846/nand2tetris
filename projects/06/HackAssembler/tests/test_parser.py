from unittest import TestCase
from hack_parser import Parser
from main import InstructionTypes

INSTRUCTIONS = ["@1", "@2", "@10", "(LOOP)", "D=M;JMP"]


class TestParser(TestCase):
    def test_has_no_more_instructions(self):
        parser = Parser(INSTRUCTIONS)
        for i in range(len(INSTRUCTIONS)):
            parser.read_and_move_cursor()
        self.assertFalse(parser.has_more_instructions())

    def test_has_more_instructions(self):
        parser = Parser(INSTRUCTIONS)
        parser.read_and_move_cursor()
        parser.read_and_move_cursor()
        self.assertTrue(parser.has_more_instructions())

    def test_get_a_instruction_type(self):
        parser = Parser(INSTRUCTIONS)
        parser.read_and_move_cursor()
        instruction_type = parser.current_instruction_type()
        self.assertEqual(InstructionTypes.A.value, instruction_type)

    def test_get_c_instruction_type(self):
        parser = Parser(INSTRUCTIONS)
        parser.read_and_move_cursor()
        parser.read_and_move_cursor()
        parser.read_and_move_cursor()
        parser.read_and_move_cursor()
        instruction_type = parser.current_instruction_type()
        self.assertEqual(InstructionTypes.C.value, instruction_type)

    def test_get_label_instruction_type(self):
        parser = Parser(INSTRUCTIONS)
        parser.read_and_move_cursor()
        parser.read_and_move_cursor()
        parser.read_and_move_cursor()
        instruction_type = parser.current_instruction_type()
        self.assertEqual(InstructionTypes.LABEL.value, instruction_type)

    def test_parse_a_instruction(self):
        parser = Parser(INSTRUCTIONS)
        instruction = parser.parse()
        self.assertEqual(instruction, INSTRUCTIONS[0])

    def test_parse_c_instruction(self):
        parser = Parser(INSTRUCTIONS)
        instruction = parser.parse()
        instruction = parser.parse()
        instruction = parser.parse()
        instruction = parser.parse()
        instruction = parser.parse()
        self.assertEqual(instruction, INSTRUCTIONS[4])

    def test_parse_label_instruction(self):
        parser = Parser(INSTRUCTIONS)
        instruction = parser.parse()
        instruction = parser.parse()
        instruction = parser.parse()
        instruction = parser.parse()
        self.assertEqual(instruction, INSTRUCTIONS[3])




