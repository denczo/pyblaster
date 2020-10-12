import configparser
from enum import Enum


class ExtendedEnum(Enum):

    @classmethod
    def names(cls):
        return list(map(lambda c: c.name, cls))

    @classmethod
    def values(cls):
        return list(map(lambda c: c.value, cls))


class OscType(ExtendedEnum):
    TRIANGLE = 1
    SAWTOOTH = 2
    SQUARE = 3
    DEFAULT = 4


class KeyboardState(ExtendedEnum):
    DEFAULT = 1
    PRESSED = 2
    RELEASED = 3


class LfoMode(ExtendedEnum):
    DEFAULT = 1
    FILTER = 2


class StateCarrier:
    def __init__(self, states):
        self._state = None
        self.states = states

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if value in self.states:
            self._state = value
        else:
            raise ValueError("Value can only be one of the following ", self.states)

    # for command attribute in tkinter widgets
    def saveVal(self, value):
        self.state = value


# tkinter needs objects to pass commands as parameter
class ValueCarrier:
    # max = stepsize, max/100*currentValue = actual value
    def __init__(self, max: float, factor=1):
        self.max = max / 100
        self._value = 0
        self._factor = factor

    @property
    def value(self):
        return float(self._value * self.max)

    # logarithmic scale, value between 0.02 and 2
    @value.setter
    def value(self, value):
        if float(value) <= 0:
            self._value = 0
        else:
            self._value = 10 ** float(value) * self._factor

    # for command attribute in tkinter widgets
    def saveVal(self, value):
        self.value = value


class DataInterface:
    def __init__(self):
        maxGain = 0.6
        self.wf_frequency = ValueCarrier(2000)  # 2000 hz
        self.wf_sawtooth = ValueCarrier(maxGain)
        self.wf_triangle = ValueCarrier(maxGain)
        self.wf_square = ValueCarrier(maxGain)

        self.ft_reverb = ValueCarrier(10000)  # m_delay
        self.ft_cutoff = ValueCarrier(1000, 0.1)  # cuttoff hz

        self.env_attack = ValueCarrier(100)
        self.env_decay = ValueCarrier(100)
        self.env_sustain = ValueCarrier(100)
        self.env_release = ValueCarrier(100)
        self.env_state = StateCarrier(KeyboardState.values())

        self.lfo_rate = ValueCarrier(20)  # 20 hz
        self.lfo_amount = ValueCarrier(100, 0.1)  # fdelta
        self.lfo_mode = StateCarrier(LfoMode.values())
        self.lfo_mode.state = LfoMode.DEFAULT.value

        self.lfo_type = StateCarrier(OscType.values())
        self.lfo_type.state = OscType.TRIANGLE.value

        self.tp_state = StateCarrier([True, False])

        self.harm_amount = 0
