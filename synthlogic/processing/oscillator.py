import numpy as np
from scipy import signal, integrate

from synthlogic.structures.value import OscType


# shifted by pi/2, so it starts at 0
def t(fc, x):
    return 2 * np.pi * fc * x - np.pi / 2


def select_waveform(type_wf, t, lfo=0):
    if type_wf == OscType.TRIANGLE.value:
        return signal.sawtooth(t + lfo, 0.5)
    elif type_wf == OscType.SAWTOOTH.value:
        return signal.sawtooth(t + lfo, 0)
    elif type_wf == OscType.SQUARE.value:
        return signal.square(t + lfo)
    else:
        return np.zeros(len(t))


# def lfo_freq(type_lfo, fm, x, fdelta=1)
#     if fm > 0:
#         beta = fdelta / fm
#         t_lfo = t(fm, x)
#         waveform = select_waveform(type_lfo, t_lfo)
#         # lfo = select_waveform(OscType.TRIANGLE, t_lfo)
#         # calculating the integral of the given waveform
#          lfo = integrate.cumtrapz(waveform, x, initial=0)
#         # lfo *= beta * 2 * np.pi
#         lfo = waveform * beta * 2 * np.pi
#         return lfo
#     else:
#         return 0


def running_sum(s, l):
    y = np.zeros(len(s))
    y[0] = s[0] + l
    for n in range(1, len(s)):
        y[n] = s[n] + y[n - 1]
    return y


def lfo(type_lfo, fm, x, l, fdelta=1):
    if fm > 0:
        beta = fdelta / fm
        t_lfo = 2 * np.pi * fm * x - np.pi
        waveform = select_waveform(type_lfo, t_lfo)
        # lfo = select_waveform(OscType.TRIANGLE, t_lfo)
        # calculating the integral of the given waveform
        # lfo = integrate.cumtrapz(waveform, t_lfo, initial=0)
        lfo = running_sum(waveform, l)
        lfo *= beta
        # lfo *= beta * 2 * np.pi
        # lfo = waveform * beta * 2 * np.pi
        return lfo
    else:
        return np.zeros(1024)


def carrier(type_wf, fc, x, lfo=0):
    t_wf = t(fc, x)
    return select_waveform(type_wf, t_wf, lfo)


def harmonics(type_wf, y, fc, x, amount, lfo=0):
    if amount > 0:
        g = 1 / amount
        # harmonics e.g. fc = 20hz; i * fc = 40, 60, 80 ...
        for i in range(2, amount + 2):
            fc_harm = fc * i
            y = np.add(y, g * carrier(type_wf, fc_harm, x, lfo))
    return y


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
