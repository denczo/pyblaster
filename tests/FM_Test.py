import numpy as np
import matplotlib.pylab as plt
from scipy import signal
from scipy import integrate


x1 = np.linspace(0, 1, 5000)
x2 = np.linspace(1, 2, 5000)
x3 = np.linspace(2, 3, 5000)
x_sum = np.linspace(0,3, 100000)

fm = 7.381
#fm = 4
fc = 40
fdelta = 100
# modulation index
beta = fdelta/fm

sine1 = np.sin(2*np.pi*fm*x1 - np.pi/2)
sine2 = np.sin(2*np.pi*fm*x2 - np.pi/2)
sine3 = np.sin(2*np.pi*fm*x3 - np.pi/2)

sawtooth = signal.sawtooth(2*np.pi*fm*x1 - np.pi/2, 1)
triangle = signal.sawtooth(2*np.pi*fm*x1 - np.pi/2, 0.5)
square1 = signal.square(2*np.pi*fm*x1 - np.pi/2)
square2 = signal.square(2*np.pi*fm*x2 - np.pi/2)
square3 = signal.square(2*np.pi*fm*x3 - np.pi/2)
square_sum = signal.square(2*np.pi*fm*x_sum - np.pi/2)

#print(len(square1), len(x1))
lfo1 = integrate.cumtrapz(square1, dx=0.0002, initial=0)*beta
lfo2 = integrate.cumtrapz(square2, dx=0.0002, initial=0)*beta
lfo3 = integrate.cumtrapz(square3, dx=0.0002, initial=0)*beta

def create_sawtooth(a, x, fc):
    result = 0
    for n in range(1, a):
        #result += (np.sin(2*np.pi*fc*n*x+10*(np.sin(2*np.pi*2*x)))/n)
        result += (np.sin(2*np.pi*fc*n*x)/n)
    return result


def running_sum(s, l):
    y = np.zeros(len(s))
    y[0] = s[0] + l
    for n in range(1, len(s)):
        y[n] = s[n] + y[n-1]
    return y

#y = np.sin(2*np.pi*fc*x1+80*lfo1)
y = 0.5*create_sawtooth(100, x1, 10)
#y = np.sin(2*np.pi*fc*x + 20*np.sin(2*np.pi*fm*x))
#y = np.sin(2*np.pi*fc*x) + np.sin(20*np.sin(2*np.pi*fm*x))

#plt.plot(x, y, label="Sine waveform with frequency modulation")
#plt.plot(x, 20*lfo, label="LFO at 4 hz")
#plt.legend(loc="upper left")
#plt.ylim(-1.5, 2.0)
# #plt.axis('off')
#plt.plot(x1, square1)

integral1 = running_sum(square1, 0)
integral2 = running_sum(square2, integral1[-1])
integral3 = running_sum(square3, integral2[-1])
integral_sum = running_sum(square_sum, 0)
#max_val = max(integral)
#min_val = min(integral)
#y = integrate - min_val / max_val - min_val
y1 = integral1 / integral1.max(axis=0)
y2 = integral2 / integral2.max(axis=0)
y3 = integral3 / integral3.max(axis=0)
y_sum = integral_sum / integral_sum.max(axis=0)

#plt.plot(x_sum, y_sum)
plt.plot(x1, y1)

plt.plot(x2, y2)
plt.plot(x3, y3)
# plt.plot(x1, lfo1)
# plt.plot(x1, square1)
#
# plt.plot(x2, sine2)
# plt.plot(x2, lfo2)
# plt.plot(x2, square2)
#
#plt.plot(x3, sine3)
# plt.plot(x3, lfo3)
# plt.plot(x3, square3)

#plt.plot(x1,y)

plt.show()
