import pyaudio
import numpy as np
from scipy import signal
import threading
from synthlogic.EnvelopeGen import EnvelopeGen
from synthlogic.Filter.Allpass import Allpass
from scipy.io import wavfile


class Synth:
    def __init__(self, rate=44100, chunk=1024, gain=0.1, fadeSeq=512):

        self.envGen = EnvelopeGen()
        self.BUFFERSIZE = 22016
        # self.envGen.setAttack(100)
        self.reverb = 1
        self.waveform = ["sine", "triangle", "sawtooth", "square"]
        self.selectedStyle = 0
        self.selectedWaveform = 0
        self.attack = []
        self.x = np.zeros(chunk)
        self.y = np.zeros(chunk)
        self.gain = gain
        self.quadratic = 0
        self.frequency = 0
        self.fadeSeq = fadeSeq
        self.coefficients = np.linspace(0, 1, fadeSeq)
        self.coefficientsR = self.coefficients[::-1]
        self.pufferX = np.zeros(self.fadeSeq)
        self.pufferY = np.zeros(self.fadeSeq)
        self.rate = int(rate)
        self.chunk = chunk
        self.buffer = np.zeros(chunk)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=rate,
                                  output=1,
                                  frames_per_buffer=chunk)
        self.stream.stop_stream()

    def setWaveform(self, val):
        self.selectedWaveform = val

    def setReverb(self, val):
        actualVal = self.convert2Value(val, self.BUFFERSIZE)
        self.reverb = actualVal

    def convert2Value(self, percentage, max):
        return max/100*int(percentage)

    def setStyle(self, val):
        self.selectedStyle = val

    def toggle(self):
        if self.stream.is_active():
            print("active")
            self.stream.stop_stream()
        elif self.stream.is_stopped():
            print("inactive")
            self.stream.start_stream()
            t = threading.Thread(target=self.render)
            t.start()

    def setFrequency(self, freq):
        self.frequency = freq

    def run(self):
        self.render()

    def signal(self, type, freq, x):
        if type == "sine":
            return np.sin(2 * np.pi * int(freq) * x)
        elif type == "sawtooth":
            return signal.sawtooth(2 * np.pi * int(freq) * x, 1)
        elif type == "square":
            return signal.square(2 * np.pi * int(freq) * x)
        elif type == "triangle":
            return signal.sawtooth(2 * np.pi * int(freq) * x, 0.5)

    def style(self, type, x, freq):
        y = self.signal(self.waveform[self.selectedWaveform], freq, x)
        waves = int(type)
        for i in range(waves):
            y = np.add(y, self.signal(self.waveform[self.selectedWaveform], int(freq) * (waves - i), x))
        return y

    def addEnvelope(self, chunk, chunkPos):

        if chunkPos < self.envGen.attackRange:
            return self.envGen.attack(chunk, chunkPos)
        else:
            return chunk

    def cleanSignal(self, signal, puffer):
        puffer = [a * b for a, b in zip(self.coefficientsR, puffer)]
        signal[:self.fadeSeq] = [a * b for a, b in zip(self.coefficients, signal[:self.fadeSeq])]
        signal[:self.fadeSeq] += puffer

        # signal[-self.fadeSeq:] = [a*b for a, b in zip(self.coefficientsR, signal[-self.fadeSeq:])]
        return signal

    def render(self):
        start = 0
        end = self.chunk
        g1 = 0.7
        g2 = 0.7
        #M = 10000
        allpass = Allpass(self.BUFFERSIZE)

        # debug
        frames = np.zeros(0)

        # TODO gemeinsames vielfaches, offset wieder bei 0 anfangen.. sonst gehts gegen unendlich
        while self.stream.is_active():
            M = int(self.reverb)
            currentFreq = self.frequency
            self.x = np.arange(start, end) / self.rate

            self.y = self.style(self.selectedStyle, self.x, currentFreq)
            # self.y = self.signal(self.waveform[self.selectedWaveform], currentFreq, self.x)
            self.y = self.cleanSignal(self.y, self.pufferY)
            self.y = self.addEnvelope(self.y, end)

            self.y = allpass.output(self.y, g1, g2, M)

            chunk = self.y * self.gain
            #frames = np.append(frames, chunk)

            self.stream.write(chunk.astype(np.float32).tostring())

            self.pufferX = np.arange(end, end + self.fadeSeq) / self.rate
            self.pufferY = self.style(self.selectedStyle, self.pufferX, currentFreq)

            start = end
            end += self.chunk

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        #wavfile.write('recorded.wav', 44100, frames)
