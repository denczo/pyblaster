import numpy as np
import matplotlib.pyplot as plt

class Test:
    def __init__(self, a):
        self._a = a
    
    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        if value < 0:
            value = 0
        self._a = value


#test = Test(5)
#print(test.a)
#test.a = -1
#print(test.a)

#x = np.arange(0, 1000)
#y = np.logspace(0, 1000)
#print(np.logspace(0, 100, 100))
#plt.plot(x,y)
#plt.show()

#print(np.logspace(0, 2, 100, base=10))
#p#rint(np.log10(1))