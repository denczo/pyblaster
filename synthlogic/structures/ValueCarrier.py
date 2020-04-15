# tkinter needs objects to pass commands as parameter
class ValueCarrier:
    def __init__(self):
        self.value = 0

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value
