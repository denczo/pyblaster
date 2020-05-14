import numpy as np
from scipy import signal, integrate

from synthlogic.oscillator.OscType import OscType


class Oscillator:

    def t(self, fc, x):
        return 2*np.pi*fc*x

    def lfo(self, typeLfo, fm, x, fdelta=5):
        if fm > 0:
            beta = fdelta/fm
            t_lfo = self.t(fm, x)
            waveform = self.selectWaveform(typeLfo, t_lfo)
            lfo = integrate.cumtrapz(waveform, x, initial=0)
            lfo *= beta*2*np.pi
            return lfo
        else:
            return 0

    def carrier(self, typeCarrier, t, gain, lfo=0):
        if gain > 1:
            raise ValueError("Value of gain too high. Maximum should be 1!")
        elif gain > 0:
            return gain * self.selectWaveform(typeCarrier, t+lfo)
        else:
            return self.selectWaveform(OscType.DEFAULT, t)

    #TODO delete
    def render(self, typeCarrier, fc, x, gain, typeLfo=None, fm=None, am=None, fdelta=1):

        if typeLfo is not None and fm is not None:
            beta = fdelta/fm
            t_lfo = 2*np.pi*fm*x
            waveform = self.selectWaveform(typeLfo, t_lfo)
            lfo = integrate.cumtrapz(waveform, x, initial=0)
            lfo *= beta*2*np.pi
        else:
            lfo = 0

        t_carrier = 2*np.pi*fc*x+lfo
        if gain > 0:
            carrier = gain * self.selectWaveform(typeCarrier, t_carrier)
        else:
            carrier = self.selectWaveform(OscType.DEFAULT, t_carrier)

        # if am is not None:
        #     lfo = np.sin(2*np.pi*am*x)
        #     carrier *= lfo

        return carrier

    @staticmethod
    def selectWaveform(type, t):
        if type == OscType.TRIANGLE:
            return signal.sawtooth(t, 0.5)
        elif type == OscType.SAWTOOTH:
            return signal.sawtooth(t, 1)
        elif type == OscType.SQUARE:
            return signal.square(t)
        else:
            return np.zeros(len(t))
