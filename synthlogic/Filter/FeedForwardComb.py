from synthlogic.Filter.CircularBuffer import CircularBuffer


class FeedForwardComb:

    def __init__(self, size, chunkSize):
        self.delayLine = CircularBuffer(size)
        # writable size
        self.size = size - chunkSize

    def output(self, x, g, M):

        if 0 < M <= self.size:
            # size of x and delayed signal need to be equally
            start = self.size - len(x) - M
            self.delayLine.add(x)
            y = x + g * self.delayLine[start:-M]
            return y
        else:
            return x
