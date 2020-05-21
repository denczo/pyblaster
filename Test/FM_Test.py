import numpy as np
import matplotlib.pylab as plt
from scipy import signal
import sympy as sp
from scipy import integrate


x = np.linspace(0, 1, 5000)
x_lfo = np.linspace(1, 2, 5000)
fm = 4
fc = 44
fdelta = 100
# modulation index
beta = fdelta/fm
#lfo = signal.sawtooth(2*np.pi*fm*x, 0.5)

triangle = signal.sawtooth(2*np.pi*fm*x, 1)
sawtooth = signal.sawtooth(2*np.pi*fm*x, 0.5)
square = signal.square(2*np.pi*fm*x_lfo)
lfo = integrate.cumtrapz(triangle, x_lfo, initial=0)

y = signal.square(2*np.pi*fc*x+2*np.pi*beta*lfo)
#y = np.sin(2*np.pi*fc*x+2*np.pi*beta*lfo)
plt.plot(x, y)
plt.plot(x, lfo)
plt.plot(x, beta*lfo)
#plt.plot(x, sawtooth)
# plt.plot(x, triangle)
# plt.plot(x, sawtooth)
# plt.plot(x, square)
plt.show()
