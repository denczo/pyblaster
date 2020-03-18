import numpy as np

class Filter:
    def __init__(self, rate=44100, chunk=1024):
        self.chunk = chunk
        self.xDelayed = np.zeros(chunk)
        self.yDelayed = np.zeros(chunk)
        self.buffer = np.zeros(chunk)

    def feedforwardComb(self, x, g, M, previousX):
        self.xDelayed = self.delayedSignal(x, previousX, M)
        return x + g*self.xDelayed

    def feedbackComb(self, x, g, M, previousY):
        #output y1
        previousY[-M:]
        # new y
        #return x[:M] + g*previousY[-M:]
        i = 1
        while M*i < self.chunk:

            
            i += 1

        #output y2
        x[:M]

        self.yDelayed = self.delayedSignal(x, previousY, M)
        return x + g*self.yDelayed

    def delayedSignal(self, signal, prevSignal, M):
        self.buffer[:M] = prevSignal[-M:]
        self.buffer[M:] = signal[:-M]
        return self.buffer

    def allpass(self, x, g1, M1, g2, M2, previousX, previosY):
        self.xDelayed = self.delayedSignal(x, previousX, M1)
        self.yDelayed = self.delayedSignal(x, previosY, M2)
        return x + g1*self.xDelayed - g2*self.yDelayed