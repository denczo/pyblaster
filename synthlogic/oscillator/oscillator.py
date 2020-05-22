import numpy as np
from scipy import signal, integrate

from synthlogic.structures.states.OscType import OscType


def t(fc, x):
    return 2 * np.pi * fc * x


def select_waveform(type_wf, t, lfo=0):
    if type_wf == OscType.TRIANGLE.value:
        return signal.sawtooth(t + lfo, 0.5)
    elif type_wf == OscType.SAWTOOTH.value:
        return signal.sawtooth(t + lfo, 1)
    elif type_wf == OscType.SQUARE.value:
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

#
# class Oscillator:
#
#     @staticmethod
#     def t(fc, x):
#         return 2 * np.pi * fc * x
#
#     @staticmethod
#     def lfo(typeLfo, fm, x, fdelta=1):
#         if fm > 0:
#             beta = fdelta / fm
#             t_lfo = Oscillator.t(fm, x)
#             waveform = Oscillator.selectWaveform(typeLfo, t_lfo)
#             lfo = integrate.cumtrapz(waveform, x, initial=0)
#             lfo *= beta * 2 * np.pi
#             return lfo
#         else:
#             return 0
#
#     def carrier(self, typeCarrier, t, lfo):
#         # if gain > 1:
#         #     raise ValueError("Value of gain too high. Maximum should be 1!")
#         # elif gain > 0:
#         #     return gain * self.selectWaveform(typeCarrier, t+lfo)
#         # else:
#         #     return self.selectWaveform(OscType.DEFAULT, t)
#         return self.selectWaveform(typeCarrier, t + lfo)
#
#     # TODO delete
#     def render(self, typeCarrier, fc, x, gain, typeLfo=None, fm=None, am=None, fdelta=1):
#
#         if typeLfo is not None and fm is not None:
#             beta = fdelta / fm
#             t_lfo = 2 * np.pi * fm * x
#             waveform = self.selectWaveform(typeLfo, t_lfo)
#             lfo = integrate.cumtrapz(waveform, x, initial=0)
#             lfo *= beta * 2 * np.pi
#         else:
#             lfo = 0
#
#         t_carrier = 2 * np.pi * fc * x + lfo
#         if gain > 0:
#             carrier = gain * self.selectWaveform(typeCarrier, t_carrier)
#         else:
#             carrier = self.selectWaveform(OscType.DEFAULT, t_carrier)
#
#         # if am is not None:
#         #     lfo = np.sin(2*np.pi*am*x)
#         #     carrier *= lfo
#
#         return carrier
#
#     @staticmethod
#     def selectWaveform(type, t, lfo=0):
#         if type == OscType.TRIANGLE:
#             return signal.sawtooth(t + lfo, 0.5)
#         elif type == OscType.SAWTOOTH:
#             return signal.sawtooth(t + lfo, 1)
#         elif type == OscType.SQUARE:
#             return signal.square(t + lfo)
#         else:
#             return np.zeros(len(t))
