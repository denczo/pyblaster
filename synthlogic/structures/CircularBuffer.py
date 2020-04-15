from numpy import *


class CircularBuffer:

    def __init__(self, maxLength, chunkSize):
        self.circularBuffer = zeros(maxLength)
        self.maxLength = maxLength
        # head
        self.bufferPos = 0
        self.readSize = chunkSize
        self.writeSize = self.maxLength - self.readSize

    def __getitem__(self, item):
        return self.circularBuffer[item]

    def __len__(self):
        return self.maxLength

    def clear(self):
        self.circularBuffer = zeros(self.maxLength)
        self.bufferPos = 0

    def add(self, x):

        # tail
        lengthBuffer = self.bufferPos + self.readSize
        # when there is enough space to save x without splitting
        if lengthBuffer <= self.maxLength:
            self.circularBuffer[self.bufferPos:lengthBuffer] = x
        # when x will exceed the buffer size and need to be split
        else:
            bufferLeft = self.maxLength - self.bufferPos
            end = self.readSize - bufferLeft
            self.circularBuffer[self.bufferPos:] = x[:bufferLeft]
            self.circularBuffer[:end] = x[bufferLeft:]

        self.bufferPos = lengthBuffer % self.maxLength
        # rolls, so that newest entries are always at the end of the circularBuffer
        self.circularBuffer = roll(self.circularBuffer, -self.bufferPos)
        self.bufferPos = 0
