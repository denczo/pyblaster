import numpy as np


class EnvelopeGen:

    def __init__(self, chunkSize=1024):
        self.chunkSize = chunkSize
        self.attackRange = 0
        self.attackValues = []

    def convert2Value(self, percentage, max):
        return max/100*int(percentage)

    def setAttack(self, value):
        max = self.chunkSize * 43
        actualValue = self.convert2Value(value, max)
        self.attackRange = actualValue
        x = np.linspace(0, 1, int(self.attackRange))
        # using exponential function
        self.attackValues = np.fromiter(map(lambda a: a**2, x), dtype=np.float32)

    # chunkPos = where chunk ends
    def attack(self, chunk, chunkPos):
        section = self.attackValues[chunkPos-self.chunkSize:chunkPos]
        return np.fromiter([a*b for a, b in zip(chunk, section)], dtype=np.float32)
