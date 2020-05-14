# tkinter needs objects to pass commands as parameter
class ValueCarrier:
    def __init__(self, max: float):
        self.max = max/100
        #self._value = 0
        self.value = 0

    def setValue(self, value):
        self.value = 10**float(value)
        #print(self.value)

    def getValue(self):
        return float(self.value*self.max)

    # @property
    # def value(self):
    #     return float(self.value*self.max)
    #
    # @value.setter
    # def value(self, value):
    #     self._value = float(value)