import numpy as np

from synthlogic.Filter.CircularBuffer import CircularBuffer


class BasicFilter:

    def __init__(self, bufferSize, rate=44100, chunk=1024):
        self.circularBuffer = CircularBuffer()
        self.chunk = chunk

    def delayLine(self, x, M):
        pass

