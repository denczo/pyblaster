# connection between gui or hardware and actual software synth
from synthlogic.oscillator.LfoMode import LfoMode
from synthlogic.structures.StateCarrier import StateCarrier
from synthlogic.structures.ValueCarrier import ValueCarrier
from synthlogic.structures.states.KeyboardState import KeyboardState
from synthlogic.structures.states.OscType import OscType


class DataInterface:
    def __init__(self):
        maxGain = 0.6
        self.wf_frequency = ValueCarrier(2000)  # 2000 hz
        self.wf_sawtooth = ValueCarrier(maxGain)
        self.wf_triangle = ValueCarrier(maxGain)
        self.wf_square = ValueCarrier(maxGain)

        self.ft_reverb = ValueCarrier(10000) # m_delay
        self.ft_cutoff = ValueCarrier(1000, 0.1) # cuttoff hz

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
