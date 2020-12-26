import numpy as np
from scipy.fft import fft
from scipy import signal

# TODO add logic to smooth out discontinuities, when M is changed
class Allpass:

    def __init__(self, size, chunkSize):
        self.delayLineY = CircularBuffer(size, chunkSize)
        self.delayLineX = CircularBuffer(size, chunkSize)
        # writable size
        self.size = size - chunkSize

    def output(self, x, g1, g2, M):

        if 0 < M <= self.size:
            # size of x and delayed signal need to be equally
            start = self.size - M
            self.delayLineX.add(x)
            y = x + g1 * self.delayLineX[start:-M] - g2 * self.delayLineY[start:-M]
            self.delayLineY.add(y)
            return y
        else:
            return x

    def smoothTransition(self):
        pass


class LowPass:

    def __init__(self, M):
        self.M = M
        self.blackmanWindow = self.calcBlackmanWindow(M)
        self.overlap = []
        self.overlap_lfo = []

    def sinc(self, x, fc):
        return np.sin(2 * np.pi * fc * x) / x

    def sincShifted(self, fc, M):
        h = np.zeros(M)
        if M % 2 == 0:
            mid = M/2
            for i in range(M):
                if i - mid == 0:
                    h[i] = 2*np.pi * fc
                else:
                    h[i] = self.sinc(i-mid, fc)
        return h

    @staticmethod
    def calcBlackmanWindow(M):
        i = np.arange(0, M)
        return 0.42 - 0.5 * np.cos(2 * np.pi * i / M) + 0.08 * np.cos(4 * np.pi * i / M)

    def filterKernel(self, fc, M):
        kernel = self.sincShifted(fc, M)
        kernel = kernel * self.blackmanWindow
        sum = np.sum(kernel)
        kernel /= sum
        return kernel

    def applyLfo(self, lfo, chunk):
        # average value
        fc = abs(np.mean(lfo))
        fc = int(fc*50)
        if fc > 0:
            fc = 0.5/fc
        else:
            fc = 0.5/0.001

        kernel = self.filterKernel(fc, self.M)
        chunk_size = 1024

        result_conv = np.convolve(chunk[:chunk_size], kernel, 'full')
        overlap_size = len(self.overlap_lfo)
        result = result_conv[:chunk_size]
        #print(len(result[:overlap_size]),len(result_conv[chunk_size:]), len(result_conv[:chunk_size]), chunk_size, overlap_size)
        result[:overlap_size] = np.add(result[:overlap_size], self.overlap_lfo)
        self.overlap_lfo = result_conv[chunk_size:]

        return result


    def apply(self, chunk, fc):
        if fc > 0:
            fc = 0.5/fc
            kernel = self.filterKernel(fc, self.M)
            chunk_size = 1024
            result_conv = np.convolve(chunk[:chunk_size], kernel, 'full')
            overlap_size = len(self.overlap)
            print(len(result_conv), len(kernel), chunk_size)
            result = result_conv[:chunk_size]
            result[:overlap_size] = np.add(result[:overlap_size], self.overlap)
            self.overlap = result_conv[chunk_size:]
            return result
        else:
            return chunk


class CircularBuffer:

    def __init__(self, maxLength, chunkSize):
        self.circularBuffer = np.zeros(maxLength)
        self.maxLength = maxLength
        # head
        self.bufferPos = 0
        self.readSize = chunkSize
        self.writeSize = self.maxLength - self.readSize

    def __getitem__(self, item):
        return self.circularBuffer[item]

    def __len__(self):
        return self.maxLength

    def clear(self):
        self.circularBuffer = np.zeros(self.maxLength)
        self.bufferPos = 0

    def add(self, x):

        # tail
        lengthBuffer = self.bufferPos + self.readSize
        # when there is enough space to save x without splitting
        if lengthBuffer <= self.maxLength:
            self.circularBuffer[self.bufferPos:lengthBuffer] = x
        # when x will exceed the buffer size and need to be split
        else:
            bufferLeft = self.maxLength - self.bufferPos
            end = self.readSize - bufferLeft
            self.circularBuffer[self.bufferPos:] = x[:bufferLeft]
            self.circularBuffer[:end] = x[bufferLeft:]

        self.bufferPos = lengthBuffer % self.maxLength
        # rolls, so that newest entries are always at the end of the circularBuffer
        self.circularBuffer = np.roll(self.circularBuffer, -self.bufferPos)
        self.bufferPos = 0