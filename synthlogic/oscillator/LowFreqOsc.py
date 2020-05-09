from synthlogic.oscillator.LfoType import LfoType


class LowFreqOsc:
    def __init__(self):
        self._rate = 0
        self._amount = 0

    @property
    def rate(self):
        return self._rate

    @property
    def amount(self):
        return self._amount

    @rate.setter
    def rate(self, value):
        # limited to 20 hz
        if 20 >= value > 0:
            self._rate = value
        elif value > 20:
            self._rate = 20
        else:
            self._rate = 0

    @amount.setter
    def amount(self, value):
        self._amount = value

    def applyLFO(self, carrier, type):

        # amplitude modulation
        if type == LfoType.VOLUME:
            return
        # frequency modulation
        elif type == LfoType.FREQUENCY:
            pass
        elif type == LfoType.CUTOFF:
            pass
        else:
            pass

    def volume(self):
        pass

    def cutoff(self):
        pass

    def frequency(self):
        pass

