import pyaudio
import numpy as np
from scipy import signal
import threading

from scipy.io import wavfile

from synthlogic.Envelope.Envelope import Envelope
from synthlogic.filter.LowPass import LowPass
from synthlogic.algorithms.EnvelopeGen import EnvelopeGen
from synthlogic.filter.Allpass import Allpass
from synthlogic.structures.ValueCarrier import ValueCarrier


class Synth:
    def __init__(self, rate=44100, chunkSize=1024, gain=0.05, fadeSeq=896):

        self.envGen = EnvelopeGen()
        self.BUFFERSIZE = 22016
        self.writeable = self.BUFFERSIZE - chunkSize
        self.waveform = ["sine", "triangle", "sawtooth", "square"]
        self.selectedStyle = 0
        self.attack = []
        self.x = np.zeros(chunkSize+fadeSeq)
        self.y = np.zeros(chunkSize+fadeSeq)
        self.buffer = np.zeros(fadeSeq)
        self.chunk = np.zeros(chunkSize)
        self.gain = gain
        self.fadeSeq = fadeSeq
        self.coefficients = np.linspace(0, 1, fadeSeq)
        self.coefficientsR = self.coefficients[::-1]

        self.rate = int(rate)
        self.chunkSize = chunkSize
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=rate,
                                  output=1,
                                  frames_per_buffer=chunkSize)
        self.stream.start_stream()
        self.running = False
        self.pressed = False
        self.status = 'PLAY'
        # setter; tkinter needs objects to pass commands as parameter
        self.valueWaveform = ValueCarrier()

        # values for waveforms
        self.valueSine = ValueCarrier()
        self.valueSawtooth = ValueCarrier()
        self.valueTriangle = ValueCarrier()
        self.valueSquare = ValueCarrier()

        # values for effects
        self.valueReverb = ValueCarrier()
        self.valueCutoff = ValueCarrier()
        self.valueFlanger = ValueCarrier()
        self.valueDelay = ValueCarrier()

        # values of envelope
        self.valueAttack = ValueCarrier()
        self.valueDecay = ValueCarrier()
        self.valueSustain = ValueCarrier()
        self.valueRelease = ValueCarrier()

        self.valueStyle = ValueCarrier()
        self.valueFrequency = ValueCarrier()
        self.valueStatus = ValueCarrier()

        self.toggle()

    def convert2Value(self, percentage, max):
        return max/100*int(percentage)

    def setStyle(self, val):
        self.selectedStyle = val

    def toggle(self):
        if self.running:
            print("inactive")
            self.status = 'PLAY'
            self.running = False
        elif not self.running:
            print("active")
            self.running = True
            self.status = 'STOP'
            #self.stream.start_stream()
            t = threading.Thread(target=self.render)
            t.start()

    def run(self):
        self.render()

    def sineWave(self, freq, x, gain):
        if gain > 0 :
            return gain * np.sin(2 * np.pi * int(freq) * x)
        else:
            return np.zeros(len(x))

    def sawtoothWave(self, freq, x, gain):
        if gain > 0:
            return gain * signal.sawtooth(2 * np.pi * int(freq) * x, 1)
        else:
            return np.zeros(len(x))

    def triangleWave(self, freq, x, gain):
        if gain > 0:
            return gain * signal.sawtooth(2 * np.pi * int(freq) * x, 0.5)
        else:
            return np.zeros(len(x))

    def squareWave(self, freq, x, gain):
        if gain > 0:
            return gain * signal.square(2 * np.pi * int(freq) * x)
        else:
            return np.zeros(len(x))

    def oscillator(self, freq, x):
        sine = self.sineWave(freq, x, int(self.valueSine.getValue())/100)
        saw = self.sawtoothWave(freq, x, int(self.valueSawtooth.getValue())/100)
        triangle = self.triangleWave(freq, x, int(self.valueTriangle.getValue())/100)
        square = self.squareWave(freq, x, int(self.valueSquare.getValue())/100)

        signal = np.sum((sine, triangle), axis=0)
        signal = np.sum((signal, saw), axis=0)
        signal = np.sum((signal, square), axis=0)

        return signal


    def style(self, type, x, freq):
        #y = self.signal(self.waveform[self.selectedWaveform], freq, x)
        y = self.oscillator(freq, x)
        waves = int(type)
        for i in range(waves):
            y = np.add(y, self.oscillator(int(freq) * (waves - i), x))
            #y = np.add(y, self.signal(self.waveform[self.selectedWaveform], int(freq) * (waves - i), x))
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
        end = self.chunkSize
        g1 = 0.4
        g2 = 0.4
        M_window = 200
        allpass = Allpass(self.BUFFERSIZE, self.chunkSize)
        lowpass = LowPass(M_window)
        envelope = Envelope(396288, self.chunkSize)
        # envelope.setAttack(81920)
        # envelope.setDecay(2048)
        # envelope.setSustain(0.5)
        # envelope.setRelease(51200)
        # envelope.updateEnvelope()

        # debug
        frames = np.zeros(0)

        while self.running:

            M_delay = int(self.convert2Value(self.valueReverb.getValue(), self.writeable))
            currentFreq = self.valueFrequency.getValue()
            currentLp = self.valueCutoff.getValue()
            envelope.setAttack(self.valueAttack.getValue())
            envelope.setDecay(self.valueDecay.getValue())
            envelope.setSustain(self.valueSustain.getValue())
            envelope.setRelease(self.valueRelease.getValue())
            envelope.updateEnvelope()

            self.x = np.arange(start, end + self.fadeSeq) / self.rate
            self.y = self.style(self.selectedStyle, self.x, currentFreq)
            self.y = lowpass.apply(self.y, int(currentLp))
            #self.y *= envelope.getEnvelope()[:self.chunkSize]
            # all modifications need to be done before cleanSignal
            self.y = self.cleanSignal(self.y, self.buffer)
            self.chunk = envelope.apply(self.valueStatus.getValue(), self.y[:self.chunkSize])
            self.chunk = allpass.output(self.chunk, g1, g2, M_delay)
            self.chunk = self.chunk * self.gain
            self.buffer = self.y[-self.fadeSeq:]

            # frames = np.append(frames, self.chunk)
            # if len(frames) > self.chunkSize * 500:
            #     self.running = False

            self.stream.write(self.chunk.astype(np.float32).tostring())

            start = end
            end += self.chunkSize

        print("NICE")
        wavfile.write('recorded.wav', 44100, frames)
