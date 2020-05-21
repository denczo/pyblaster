from tkinter import Scale, Tk

import numpy as np
import matplotlib.pyplot as plt

class Test:
    def __init__(self, a):
        self._a = a

    @property
    def a(self):
        print("TEST")
        return self._a

    @a.setter
    def a(self, value):
        print(value)
        if value < 0:
            value = 0
        self._a = value

    def saveVal(self, value):
        print(value)
        self._a = value

test = Test(5)
master = Tk()
a = Scale(master, from_=2, to=0, resolution=0.02, length=100, command=test.saveVal).pack()
master.mainloop()

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