from synthlogic.Filter.CircularBuffer import CircularBuffer


class FeedbackComb:

    def __init__(self, size):
        self.delayLine = CircularBuffer(size)
        self.size = size

    def output(self, x, g, M):
        # size of x and delayed signal need to be equally
        start = self.size - len(x) - M
        y = x + g * self.delayLine[start:-M]
        self.delayLine.add(y)
        return y
