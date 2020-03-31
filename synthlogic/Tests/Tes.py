import numpy as np

x = np.array([1, 2, 3, 4, 5, 7, 8])
y = np.array([1, 1, 1, 1])
#y = y * 0.5
#print(y)
z = np.convolve(x, y, 'same')

print(z)

#print(x)