from enum import Enum


class InstructionTypes(Enum):
    """Provides the mapping from Instruction Type to single char code."""

    A = "A"
    C = "C"
    LABEL = "L"
    IGNORE = "I"
