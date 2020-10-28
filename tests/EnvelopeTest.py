import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 1024)/44100
envRange = np.ones(1024)
y = np.sin(2*np.pi*50*x)

phaseRange = int(len(envRange)/4)


# everything to max
attack = np.linspace(0, 1, phaseRange)
decay = np.linspace(1, 0.5, phaseRange)
sustain = np.empty(phaseRange)
sustain.fill(0.5)
release = np.linspace(0.5, 0, phaseRange)

envelope = np.concatenate((attack, decay, sustain))
envelope = np.concatenate((envelope, release))
print(envelope)

envRange *= envelope

plt.plot(x, envRange)
plt.show()