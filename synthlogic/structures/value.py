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
    def __init__(self, max: float, factor=1, label='default'):
        self.label = label
        self.max = max / 100
        self._value = 0
        self._factor = factor

    @property
    def value(self):
        return float(self._value)

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def value_log(self):
        return float(self._value) * self.max

    # logarithmic scale, value between 0.02 and 2
    @value_log.setter
    def value_log(self, value):
        if float(value) <= 0:
            self._value = 0
        else:
            self._value = 10 ** float(value) * self._factor

    # for command attribute in tkinter widgets
    def saveVal(self, value):
        self.value = value


class ChunkFactory:
    def __init__(self, rate, fade_seq):
        self.rate = rate
        self.fade_seq = fade_seq

    def createChunk(self, x, start, end):
        pass


class DataInterface:
    def __init__(self):
        maxGain = 0.6
        self.wf_frequency = ValueCarrier(2000)
        self.wf_type = StateCarrier(OscType.values())

        self.ft_reverb = ValueCarrier(10000)  # m_delay
        self.ft_cutoff = ValueCarrier(1000, 0.1)  # cuttoff hz

        self.env_attack = ValueCarrier(10)
        self.env_decay = ValueCarrier(100)
        self.env_sustain = ValueCarrier(0.2)
        self.env_release = ValueCarrier(100)

        self.lfo_rate = ValueCarrier(20)  # 20 hz
        self.lfo_amount = ValueCarrier(100, 0.1)  # fdelta
        self.lfo_mode = StateCarrier(LfoMode.values())
        self.lfo_mode.state = LfoMode.DEFAULT.value

        self.lfo_type = StateCarrier(OscType.values())
        self.lfo_type.state = OscType.TRIANGLE.value

        self.tp_state = StateCarrier([True, False])
        self.kb_state = StateCarrier([True, False])

        self.harm_amount = 0
        self.wf_type.state = OscType.TRIANGLE.value
