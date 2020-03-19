from synthlogic.Filter.CircularBuffer import CircularBuffer


class FeedForwardComb:

    def __init__(self, size):
        self.delayLine = CircularBuffer(size)
        self.size = size

    def output(self, x, g, M):
        # size of x and delayed signal need to be equally
        start = self.size - len(x) - M
        self.delayLine.add(x)
        y = x + g * self.delayLine[start:-M]
        return y
