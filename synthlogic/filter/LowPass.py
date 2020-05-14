import numpy as np

# TODO CLEAN UP!!!
class LowPass:

    def __init__(self, M):
        self.M = M
        self.blackmanWindow = self.calcBlackmanWindow(M)

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

    def calcBlackmanWindow(self, M):
        i = np.arange(0, M)
        return 0.42 - 0.5 * np.cos(2 * np.pi * i / M) + 0.08 * np.cos(4 * np.pi * i / M)

    def filterKernel(self, fc, M):
        kernel = self.sincShifted(fc, M)
        kernel = kernel * self.blackmanWindow
        sum = np.sum(kernel)
        kernel /= sum
        return kernel

    def applyLfo(self, lfo, chunk):

        #result = np.zeros(len(chunk))
        # average value
        fc = abs(np.mean(lfo))
        fc = int(fc*100)
        #print(fc)
        if fc > 0:
            fc = 0.5/fc
            kernel = self.filterKernel(fc, self.M)
            result = np.convolve(chunk, kernel, 'same')
            return result
        else:
            return chunk

    def apply(self, chunk, fc):
        #print(fc)
        if fc > 0:
            fc = 0.5/fc
            kernel = self.filterKernel(fc, self.M)
            result = np.convolve(chunk, kernel, 'same')
            return result
        else:
            return chunk
