from synthlogic.Filter.CircularBuffer import CircularBuffer

class BasicFilter(object):

    def __init__(self, M, chunk=1024):
        self.circularBuffer = CircularBuffer(chunk*2)
        self.bufferLength = self.circularBuffer.maxLength
        self.chunk = chunk
        self.M = M

    #TODO declare start:-M, in case bufferlength > chunk+M
    def delayLine(self, M):
        return self.circularBuffer[self.bufferLength-self.chunk-M:-M]