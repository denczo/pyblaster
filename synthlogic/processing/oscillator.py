import numpy as np
from scipy import signal, integrate

from synthlogic.structures.value import OscType


# shifted by pi/2, so it starts at 0
def t(fc, x):
    return 2 * np.pi * fc * x - np.pi/2


def select_waveform(type_wf, t, lfo=0):
    if type_wf == OscType.TRIANGLE:
        return signal.sawtooth(t + lfo, 0.5)
    elif type_wf == OscType.SAWTOOTH:
        return signal.sawtooth(t + lfo, 0)
    elif type_wf == OscType.SQUARE:
        return signal.square(t + lfo)
    else:
        return np.zeros(len(t))


def lfo(type_lfo, fm, x, fdelta=1):
    if fm > 0:
        beta = fdelta / fm
        t_lfo = t(fm, x)
        waveform = select_waveform(type_lfo, t_lfo)
        lfo = integrate.cumtrapz(waveform, x, initial=0)
        lfo *= beta * 2 * np.pi
        return lfo
    else:
        return 0


def carrier(type_wf, gain, t):
    if gain > 1:
        raise ValueError("Value of gain too high. Maximum should be 1!")
    elif gain > 0.01:
        return gain * select_waveform(type_wf, t)
    else:
        return select_waveform(OscType.DEFAULT, t)


class Smoother:
    def __init__(self, fadeSeq):
        self.fadeSeq = fadeSeq
        self._buffer = np.zeros(fadeSeq)
        self.coefficients = np.linspace(0, 1, fadeSeq)
        self.coefficientsR = self.coefficients[::-1]

    @property
    def buffer(self):
        return self._buffer

    @buffer.setter
    def buffer(self, value):
        sizeValue = len(value)
        if sizeValue == self.fadeSeq:
            self._buffer = value
        else:
            raise AttributeError("size of parameter {} doesn't fit size of buffer {}".format(sizeValue, self.fadeSeq))

    # smooths transition between chunks to prevent discontinuities
    def smoothTransition(self, signal):
        buffer = [a * b for a, b in zip(self.coefficientsR, self.buffer)]
        signal[:self.fadeSeq] = [a * b for a, b in zip(self.coefficients, signal[:self.fadeSeq])]
        signal[:self.fadeSeq] += buffer
        return signal
