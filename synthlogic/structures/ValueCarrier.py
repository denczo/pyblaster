# tkinter needs objects to pass commands as parameter
class ValueCarrier:
    def __init__(self, max: float):
        self.max = max/100
        self._value = 0

    @property
    def value(self):
        #print(self._value*self.max)
        return float(self._value*self.max)

    @value.setter
    def value(self, value):
        self._value = 10**float(value)

    # for command attribute in tkinter widgets
    def saveVal(self, value):
        self.value = value
