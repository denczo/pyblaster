import numpy as np
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.disable())

from synthlogic.envelope.KeyboardState import KeyboardState

# TODO BUGFIXING!!
class Envelope:
    def __init__(self, maxRange, chunkSize):
        self.maxRange = maxRange
        self.maxPhase = self.maxRange/3
        self.chunkSize = chunkSize
        self.phasePressed = np.zeros(maxRange*2)
        self.phaseReleased = np.zeros(maxRange)
        self.phaseStart = 0
        self.phaseEnd = chunkSize
        self.attack = []
        self.decay = []
        self.sustain = 0
        self.release = []
        self.releaseRange = 0
        self.reachedMax = 0
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
        self.releaseRange = value
        self.release = np.linspace(self.sustain, 0, self.releaseRange)

    def updateRelease(self, reachedMax):
        self.releaseRange = int(self.releaseRange * reachedMax)
        self.release = np.linspace(reachedMax, 0, self.releaseRange)
        self.phaseReleased = self.resizePhase(self.release)
        #print(reachedMax)

    def convert2Value(self,  percentage, max):
        return max / 100 * int(percentage)

    def updateEnvelope(self):
        mergedPhases = np.concatenate((self.attack, self.decay))
        self.phasePressed = self.resizePhase(mergedPhases)
        self.phaseReleased = self.resizePhase(self.release)

    def resizePhase(self, phase):
        sizePhase = len(phase)
        # always round up to next bigger number
        countChunks = int(sizePhase/self.chunkSize + (sizePhase % self.chunkSize > 0))
        resizedPhase = np.zeros(countChunks*self.chunkSize)
        resizedPhase[:sizePhase] = phase
        return resizedPhase

    def updateSlicePos(self):
        self.phaseStart = self.phaseEnd
        self.phaseEnd += self.chunkSize

    def apply(self, pressed, chunk):

        if self.phase == KeyboardState.PRESSED:

            sizePhase = len(self.phasePressed)

            try:
                if self.phaseEnd < sizePhase:
                    logging.info("ATTACK/DECAY PHASE")
                    slicedPhase = self.phasePressed[self.phaseStart:self.phaseEnd]
                    # reached maximum value of attack/decay phase
                    self.reachedMax = slicedPhase[-1]
                    self.updateRelease(self.reachedMax)
                    self.updateSlicePos()
                    modification = slicedPhase
                else:
                    logging.info("SUSTAIN PHASE")
                    modification = self.sustain

                if not pressed:
                    self.phase = KeyboardState.RELEASED
                    self.phaseEnd = 0
                    self.updateSlicePos()

                return chunk * modification

            except ValueError:
                print("Lists may have different sizes. envelope (pressed) was not applied!")
                return chunk

        elif self.phase == KeyboardState.RELEASED:

            logging.info("RELEASE PHASE")
            sizePhase = len(self.phaseReleased)

            try:
                if self.phaseEnd < sizePhase:
                    #TODO phaseReleased wrong values, not starting with reachedMax
                    #print(self.reachedMax, self.sustain)
                    slicedPhase = self.phaseReleased[self.phaseStart:self.phaseEnd]
                    self.updateSlicePos()
                    modification = slicedPhase
                else:
                    self.phase = KeyboardState.DEFAULT
                    modification = 0

                if pressed:
                    self.phase = KeyboardState.PRESSED
                    self.phaseEnd = 0
                    self.updateSlicePos()

                return chunk * modification

            except ValueError:
                print("Lists may have different sizes. envelope (released) was not applied!")
                return chunk

        else:
            logging.info("DEFAULT PHASE")

            if pressed:
                self.phase = KeyboardState.PRESSED
                self.phaseEnd = 0
                self.updateSlicePos()

            return chunk * 0
