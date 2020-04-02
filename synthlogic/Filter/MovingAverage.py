from synthlogic.Filter.CircularBuffer import CircularBuffer
import numpy as np


class MovingAverage:

    def __init__(self, size, chunksize):
        self.delayLine = CircularBuffer(size, chunksize)
        self.size = size
        self.reservedBuffer = chunksize
        self.availBuffer = self.size - chunksize

    def output(self, x, M):
        kernel = np.ones(M)/M
        return np.convolve(x, kernel, 'same')
