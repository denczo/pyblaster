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


test = Test(5)
print(test.a)
test.a = -1
print(test.a)
