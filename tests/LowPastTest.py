import matplotlib.pyplot as plt
import numpy as np


def hammingWindow(M):
    x = np.arange(0, M)
    return 0.54 - 0.46 * np.cos(2 * np.pi * x / M)

def sinc(x, fc):
    return np.sin(2 * np.pi * fc * x) / x


def sincShifted(fc, M):
    h = np.zeros(M)
    if M % 2 == 0:
        mid = M / 2
        for i in range(M):
            if i - mid == 0:
                h[i] = 2 * np.pi * fc
            else:
                h[i] = sinc(i - mid, fc)
    return h


def calcBlackmanWindow(M):
    i = np.arange(0, M)
    return 0.42 - 0.5 * np.cos(2 * np.pi * i / M) + 0.08 * np.cos(4 * np.pi * i / M)


def filterKernel(fc, M):
    kernel = sincShifted(fc, M)
    kernel *= calcBlackmanWindow(M)
    sum = np.sum(kernel)
    kernel /= sum
    return kernel


M = 300
#x = np.arange(0, 100, 0.01)
#xsin = np.linspace(0, 1, 1024)
xsin = np.arange(0, 1024) / 44100
sine500 = np.sin(2*np.pi * 300 * xsin)
sine600 = np.sin(2*np.pi * 556 * xsin)
sine750 = np.sin(2*np.pi * 750 * xsin)
sine999 = np.sin(2*np.pi * 999 * xsin)

signal = np.add(sine500, sine600)
#signal = np.add(signal, sine999)
y = filterKernel(0.01, M)
convolved = np.convolve(signal, y, 'same')
filteredSignal = np.zeros(1024)
#filteredSignal[M-1:] = convolved

plt.plot(xsin, sine500)
plt.plot(xsin, signal)
plt.plot(xsin, convolved)

plt.show()
