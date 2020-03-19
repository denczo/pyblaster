from synthlogic.Filter.CircularBuffer import CircularBuffer


class Allpass:

    def __init__(self, size):
        self.delayLineY = CircularBuffer(size)
        self.delayLineX = CircularBuffer(size)
        self.size = size

    def output(self, x, g1, g2, M):
        # size of x and delayed signal need to be equally
        start = self.size - len(x) - M
        self.delayLineX.add(x)
        y = x + g1 * self.delayLineX[start:-M] - g2 * self.delayLineY[start:-M]
        self.delayLineY.add(y)
        return y
