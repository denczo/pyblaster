import numpy as np
import logging
import time

from synthlogic.structures.value import KeyboardState


# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.disable())

class Envelope:
    def __init__(self, maxRange, chunkSize):
        self.maxRange = maxRange
        self.maxPhase = self.maxRange / 3
        self.chunkSize = chunkSize
        self.phasePressed = np.zeros(maxRange * 2)
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
        actualRange = int(self.releaseRange * reachedMax)
        self.release = np.linspace(reachedMax, 0, actualRange)
        self.phaseReleased = self.resizePhase(self.release)

    def convert2Value(self, percentage, max):
        return max / 100 * percentage

    def updateEnvelope(self):
        mergedPhases = np.concatenate((self.attack, self.decay))
        self.phasePressed = self.resizePhase(mergedPhases)
        # self.phaseReleased = self.resizePhase(self.release)

    def resizePhase(self, phase):
        sizePhase = len(phase)
        # always round up to next bigger number
        countChunks = int(sizePhase / self.chunkSize + (sizePhase % self.chunkSize > 0))
        resizedPhase = np.zeros(countChunks * self.chunkSize)
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
                    # logging.info("ATTACK/DECAY PHASE")
                    slicedPhase = self.phasePressed[self.phaseStart:self.phaseEnd]
                    # reached maximum value of attack/decay phase
                    self.reachedMax = slicedPhase[-1]
                    self.updateRelease(self.reachedMax)
                    self.updateSlicePos()
                    modification = slicedPhase
                else:
                    # logging.info("SUSTAIN PHASE")
                    modification = self.sustain
                    self.updateRelease(self.sustain)

                if not pressed:
                    self.phase = KeyboardState.RELEASED
                    self.phaseEnd = 0
                    self.updateSlicePos()

                return chunk * modification

            except ValueError:
                print("Lists may have different sizes. envelope (pressed) was not applied!")
                return chunk

        elif self.phase == KeyboardState.RELEASED:

            # logging.info("RELEASE PHASE")
            sizePhase = len(self.phaseReleased)

            try:
                if self.phaseEnd < sizePhase:
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
            # print("DEFAULT PHASE")
            # logging.info("DEFAULT PHASE")

            if pressed:
                self.phase = KeyboardState.PRESSED
                self.phaseEnd = 0
                self.updateSlicePos()

            return chunk * 0


class EnvState:

    def __init__(self):
        self.currentGain = 0.001

    def next(self, input):
        return self.map[input]

    def run(self, x, x1, y1, x2, y2):
        return y1 + (x - x1) * (y2 - y1) / (x2 - x1)


attack = 0.2
decay = 0.1
sustain = 0.8
release = 0.4

test = time.time()


def calcAmplitude(self, gain1, chunkPos1, gain2, chunkPos2, current):
    return chunkPos1 + (current - gain1) * (chunkPos2 - chunkPos1) / (gain2 - gain1)


class Env:

    def __init__(self):
        self.attack_phase = 0.5
        self.decay_phase = 0.25
        self.sustain_phase = 2
        self.sustain_level = 0.5
        self.release_phase = 1

        self.reached_gain = 0
        self.main_gain = 1

        self.p_start_time = time.time()
        self.r_start_time = time.time()
        self.pressed_time = 0
        self.released_time = 0

    def apply(self, pressed):

        main_gain = 1
        gain = 0
        if pressed:
            self.pressed_time = time.time() - self.p_start_time
            self.r_start_time = time.time()
            self.released_time = 0

            # attack
            if self.pressed_time <= self.attack_phase:
                gain = self.pressed_time / self.attack_phase
            # decay
            elif self.pressed_time <= self.attack_phase + self.decay_phase:
                gain = main_gain - (self.pressed_time - self.attack_phase) / self.decay_phase * (
                        main_gain - self.sustain_level)
            # sustain
            elif self.pressed_time > self.attack_phase + self.decay_phase:
                gain = self.sustain_level
                self.sustain_phase = self.pressed_time - (self.attack_phase + self.decay_phase)

            self.reached_gain = gain
        else:
            self.released_time = time.time() - self.r_start_time
            self.p_start_time = time.time()
            self.pressed_time = 0

            # release
            if self.released_time <= self.attack_phase:
                gain = (self.attack_phase - self.released_time) / self.attack_phase * self.reached_gain
            elif self.released_time <= self.attack_phase + self.decay_phase:
                gain = (self.decay_phase - (
                        self.released_time - self.attack_phase)) / self.decay_phase * self.reached_gain
            else:
                gain = (self.release_phase - (
                            self.released_time - self.sustain_phase - self.attack_phase - self.decay_phase)) / self.release_phase * self.sustain_level

            if gain < 0.001:
                gain = 0

        return gain
