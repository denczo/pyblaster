from enum import auto

from synthlogic.structures.states.ExtendedEnum import ExtendedEnum


class KeyboardState(ExtendedEnum):
    DEFAULT = auto()
    PRESSED = auto()
    RELEASED = auto()
