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

    def average(self, x, M, pos):
        size = len(x)
        end = int(M/2) + pos
        start = end - M

        if end > size:
            end = size
        elif start < 0:
            start = 0
            #return np.sum(np.concatenate((self.delayLine[start:], x[:end]), axis=None))

        return np.sum(x[start:end])/M

