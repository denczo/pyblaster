import numpy as np


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
