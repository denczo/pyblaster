# tkinter needs objects to pass commands as parameter
class ValueCarrier:
    def __init__(self, max: float, factor=1):
        self.max = max/100
        self._value = 0
        self._factor = factor

    @property
    def value(self):
        return float(self._value*self.max)

    @value.setter
    def value(self, value):
        if float(value) <= 0:
            self._value = 0
        else:
            self._value = 10**float(value)*self._factor

    # for command attribute in tkinter widgets
    def saveVal(self, value):
        self.value = value
