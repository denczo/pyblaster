import numpy as np

from synthlogic.Envelope.KeyboardState import KeyboardState


class Envelope:
    def __init__(self, maxRange, chunkSize):
        self.maxRange = maxRange
        self.maxPhase = self.maxRange/3
        self.chunkSize = chunkSize
        self.envelope = np.zeros(maxRange)
        self.attack = []
        self.decay = []
        self.sustain = 0
        self.release = []
        self.envPos = 0
        self.releasePos = 0
        self.envSize = 0
        self.phase = KeyboardState.DEFAULT

    def setAttack(self, range):
        value = int(self.convert2Value(range, self.maxPhase))
        self.attack = np.linspace(0, 1, value)

    def setDecay(self, range):
        value = int(self.convert2Value(range, self.maxPhase))
        self.decay = np.linspace(1, self.sustain, value)

    def setSustain(self, value):
        value = self.convert2Value(value, 1)
        self.sustain = value

    def setRelease(self, range):
        value = int(self.convert2Value(range, self.maxPhase))
        self.release = np.linspace(self.sustain, 0, value)

    def convert2Value(self,  percentage, max):
        return max / 100 * int(percentage)

    def updateEnvelope(self):
        values = np.concatenate((self.attack, self.decay, self.release))
        self.envSize = len(values)
        self.releasePos = self.envSize - len(self.release)
        self.envelope[:self.envSize] = values

    def apply(self, pressed, chunk):

        # state machine
        if self.phase == KeyboardState.PRESSED:

            if not pressed:
                self.envPos = self.releasePos
                self.phase = KeyboardState.RELEASED

            if self.envPos < self.releasePos:
                start = self.envPos
                end = start + self.chunkSize
                self.envPos = end
                return chunk * self.envelope[start:end]
            else:
                return chunk * self.sustain

        elif self.phase == KeyboardState.RELEASED:

            if pressed:
                self.phase = KeyboardState.PRESSED

            if self.envPos < self.envSize:
                start = self.envPos
                end = start + self.chunkSize
                self.envPos = end
                return chunk * self.envelope[start:end]
            else:
                self.envPos = 0
                self.phase = KeyboardState.DEFAULT
                return chunk * 0

        else:
            if pressed:
                self.phase = KeyboardState.PRESSED

            return chunk * 0
