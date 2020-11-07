import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

x = np.linspace(0, 1, 7040)
base_freq = 2
second_freq = 2*base_freq
third_freq = 3*base_freq
fourth_freq = 4*base_freq

triangle1 = signal.sawtooth(2*np.pi*base_freq*x, 0.5)*0.25
triangle2 = signal.sawtooth(2*np.pi*second_freq*x, 0.5)*0.25
triangle3 = signal.sawtooth(2*np.pi*third_freq*x, 0.5)*0.25
triangle4 = signal.sawtooth(2*np.pi*fourth_freq*x, 0.5)*0.25


def create_harmonics(base_freq, amount):
    if amount > 0:
        gain = 1/amount
        fig, axs = plt.subplots(amount+1)
        combined = np.zeros(len(x))
        for i in range(1, amount+1):
            freq = base_freq * i
            wf = np.sin(2*np.pi*freq*x)*gain
            #wf = signal.sawtooth(2*np.pi*freq*x, 0.5)*gain
            combined = np.add(combined, wf)
            #plt.plot(x, wf, label=str(freq)+" hz")
            axs[i-1].plot(x, wf)
            axs[i-1].axis('off')
            axs[i - 1].legend([str(freq*110*2)+" hz"], bbox_to_anchor=(-0.17, 0.9), loc="upper left")
        axs[amount].plot(x, combined)
        axs[amount].axis('off')
        axs[amount].legend(["result"], bbox_to_anchor=(-0.17, 0.9), loc="upper left")


create_harmonics(2, 4)

plt.show()