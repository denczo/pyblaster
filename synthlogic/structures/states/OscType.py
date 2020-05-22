from enum import auto
from synthlogic.structures.states.ExtendedEnum import ExtendedEnum


class OscType(ExtendedEnum):
    TRIANGLE = auto()
    SAWTOOTH = auto()
    SQUARE = auto()
    DEFAULT = auto()
