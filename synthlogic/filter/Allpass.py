from synthlogic.structures.CircularBuffer import CircularBuffer


class Allpass:

    def __init__(self, size, chunkSize):
        self.delayLineY = CircularBuffer(size, chunkSize)
        self.delayLineX = CircularBuffer(size, chunkSize)
        # writable size
        self.size = size - chunkSize

    def output(self, x, g1, g2, M):

        if 0 < M <= self.size:
            # size of x and delayed signal need to be equally
            start = self.size - M
            self.delayLineX.add(x)
            y = x + g1 * self.delayLineX[start:-M] - g2 * self.delayLineY[start:-M]
            self.delayLineY.add(y)
            return y
        else:
            return x

    def smoothTransition(self):
        pass