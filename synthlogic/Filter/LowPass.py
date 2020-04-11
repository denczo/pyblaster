import numpy as np


class LowPass:

    def __init__(self, M):
        self.M = M
        self.blackmanWindow = self.calcBlackmanWindow(M)

    def sinc(self, x, fc):
        return np.sin(2 * np.pi * fc * x) / x

    def sincShifted(self, fc, M):
        h = np.zeros(M)
        if M % 2:
            mid = M/2
            for i in range(M):
                if i - mid == 0:
                    h[i] = 2*np.pi * fc
                else:
                    h[i] = self.sinc(i-mid, fc)
        return h

    def calcBlackmanWindow(self, M):
        i = np.arange(0, M)
        return 0.42 - 0.5 * np.cos(2 * np.pi * i / M) + 0.08 * np.cos(4 * np.pi * i / M)

    def filterKernel(self, fc, M):
        kernel = self.sincShifted(fc, M)
        kernel *= self.blackmanWindow(M)
        return kernel

    def apply(self, chunk, fc):
        kernel = self.filterKernel(fc, self.M)
        return np.convolve(chunk, kernel, 'same')