from synthlogic.Filter.BasicFilter import BasicFilter


class FeedforwardComb(BasicFilter):

    def __init__(self, g, M, chunk):
        super().__init__(M, chunk)
        self.g = g

    def output(self, x, g, M):
        self.circularBuffer.add(x)
        return x + g * self.delayLine(M)
