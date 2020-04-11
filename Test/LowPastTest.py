import matplotlib.pyplot as plt
import numpy as np


#
# def sinc(h, fc, M):
#     return np.sin(2 * np.pi * fc * (h - M / 2)) / (h - M / 2)
#

def sinc(x, fc):
    return np.sin(2 * np.pi * fc * x) / x


def shift(fc, M, K):
    result = np.zeros(M)
    for i in range(len(x)):
        if i - M / 2 == 0:
            print(i, "is zero")
            result[i] = K * 2 * np.pi * fc
        else:
            val = i - M / 2
            result[i] = K * sinc(val, fc)

    return result


def hammingWindow(h, M):
    x = np.arange(0, M)
    return 0.54 - 0.46 * np.cos(2 * np.pi * x / M)


def blackmanWindow(h, M):
    x = np.arange(0, M)
    return 0.42 - 0.5 * np.cos(2 * np.pi * x / M) + 0.08 * np.cos(4 * np.pi * x / M)


M = 1000
x = np.arange(0, 100, 0.1)
y = shift(0.02, M, 0.1)
y = y * blackmanWindow(x, M)

plt.plot(x, y)

plt.show()
