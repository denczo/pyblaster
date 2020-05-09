from enum import Enum, auto


class OscType(Enum):
    SINE = auto()
    TRIANGLE = auto()
    SAWTOOTH = auto()
    SQUARE = auto()
    DEFAULT = auto()
