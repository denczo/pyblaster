from numpy import *

class CircularBuffer:

    def __init__(self, maxLength):
        self.circularBuffer = zeros(maxLength)
        self.maxLength = maxLength
        self.bufferPos = 0

    def add(self, x):

        lengthX = len(x)
        lengthBuffer = self.bufferPos + lengthX

        if lengthBuffer <= self.maxLength:
            self.circularBuffer[self.bufferPos:lengthBuffer] = x
        else:
            bufferLeft = self.maxLength - self.bufferPos
            end = lengthX - bufferLeft
            self.circularBuffer[self.bufferPos:] = x[:bufferLeft]
            self.circularBuffer[:end] = x[bufferLeft:]

        self.bufferPos = lengthBuffer % self.maxLength

# testBuffer = CircularBuffer(10)
#
# x = arange(0,5)
# y = arange(10,17)
# z = arange(20,27)
# testBuffer.add(x)
# print(testBuffer.circularBuffer)
# testBuffer.add(y)
# print(testBuffer.circularBuffer)
# testBuffer.add(z)
# print(testBuffer.circularBuffer)