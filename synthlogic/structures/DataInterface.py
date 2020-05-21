# connection between gui or hardware and actual software synth
from synthlogic.oscillator.LfoMode import LfoMode
from synthlogic.structures.StateCarrier import StateCarrier
from synthlogic.structures.ValueCarrier import ValueCarrier
from synthlogic.structures.states.KeyboardState import KeyboardState
from synthlogic.structures.states.OscType import OscType


class DataInterface:
    def __init__(self):
        maxGain = 0.8
        self.wf_frequency = ValueCarrier(2000)  # 2000 hz
        self.wf_sawtooth = ValueCarrier(maxGain)
        self.wf_triangle = ValueCarrier(maxGain)
        self.wf_square = ValueCarrier(maxGain)

        self.ft_reverb = ValueCarrier(10000) # m_delay
        self.ft_cutoff = ValueCarrier(1000) # cuttoff hz

        self.env_attack = ValueCarrier(100)
        self.env_decay = ValueCarrier(100)
        self.env_sustain = ValueCarrier(100)
        self.env_release = ValueCarrier(100)
        self.env_state = StateCarrier(KeyboardState.list)

        self.lfo_rate = ValueCarrier(20)  # 20 hz
        self.lfo_amount = ValueCarrier(100)  # fdelta
        self.lfo_mode = StateCarrier(LfoMode.list())

        self.lfo_type = StateCarrier(OscType.list())
        # self.lfo_triangle = StateCarrier([False, True])
        # self.lfo_sawtooth = StateCarrier()
        # self.lfo_square = StateCarrier()

        self.tp_state = StateCarrier([True, False])

