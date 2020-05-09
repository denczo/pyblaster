import pyaudio
import numpy as np
import threading
import queue


from scipy.io import wavfile

from synthlogic.envelope.Envelope import Envelope
from synthlogic.filter.LowPass import LowPass
from synthlogic.filter.Allpass import Allpass
from synthlogic.oscillator.OscType import OscType
from synthlogic.oscillator.Oscillator import Oscillator
from synthlogic.oscillator.Smoother import Smoother
from synthlogic.structures.ValueCarrier import ValueCarrier


class Synth:
    def __init__(self, rate=44100, chunkSize=1024, gain=0.07, fadeSeq=896):

        self.BUFFERSIZE = 22016
        self.writeable = self.BUFFERSIZE - chunkSize
        self.waveform = ["sine", "triangle", "sawtooth", "square"]
        self.selectedStyle = 0
        self.x = np.zeros(chunkSize+fadeSeq)
        self.y = np.zeros(chunkSize+fadeSeq)
        self.chunk = np.zeros(chunkSize)
        self.gain = gain
        self.fadeSeq = fadeSeq
        self.queue = queue.LifoQueue()
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

        # setter; tkinter needs objects to pass commands as parameter
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

        # values of lfo
        self.valueLfoRate = ValueCarrier()
        self.valueLfoAmount = ValueCarrier()
        self.valueLfoType = ValueCarrier()

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
            self.running = False
        elif not self.running:
            print("active")
            self.running = True
            t = threading.Thread(target=self.render)
            t.start()

    def run(self):
        self.render()

    def style(self, type, x, freq):
        y = self.oscillator(freq, x)
        #waves = int(type)
        #for i in range(waves):
        #    y = np.add(y, self.oscillator(int(freq) * (waves - i), x))
        return y

    def render(self):
        start = 0
        end = self.chunkSize
        g1 = 0.4
        g2 = 0.4
        M_window = 200
        allpass = Allpass(self.BUFFERSIZE, self.chunkSize)
        lowpass = LowPass(M_window)
        envelope = Envelope(396288, self.chunkSize)
        smoother = Smoother(self.fadeSeq)
        osc = Oscillator()

        # debug
        frames = np.zeros(0)
        lock = threading.Lock()

        while self.running:
            M_delay = int(self.convert2Value(self.valueReverb.getValue(), self.writeable))
            currentFreq = 100
            #currentFreq = self.valueFrequency.getValue()
            currentLp = self.valueCutoff.getValue()
            envelope.setAttack(self.valueAttack.getValue())
            envelope.setDecay(self.valueDecay.getValue())
            envelope.setSustain(self.valueSustain.getValue())
            envelope.setRelease(self.valueRelease.getValue())
            envelope.updateEnvelope()

            self.x = np.arange(start, end + self.fadeSeq) / self.rate
            #self.y = self.style(self.selectedStyle, self.x, (currentFreq+Oscillator.triangle(0.25,5, self.x)))

            tri = osc.render(OscType.TRIANGLE, currentFreq, self.x, int(self.valueTriangle.getValue())/100, typeLfo=OscType.SAWTOOTH, fm=22)
            saw = osc.render(OscType.SAWTOOTH, currentFreq, self.x, int(self.valueSawtooth.getValue())/100, typeLfo=OscType.SAWTOOTH, fm=22)
            square = osc.render(OscType.SQUARE, currentFreq, self.x, int(self.valueSquare.getValue())/100, typeLfo=OscType.SAWTOOTH, fm=22)
            sum = np.sum((tri, saw), axis=0)
            sum = np.sum((sum, square), axis=0)
            self.y = sum
            #self.y = osc.render(OscType.SQUARE, currentFreq, self.x, int(self.valueSquare.getValue())/100)
            self.y = lowpass.applyLfo(osc.selectWaveform(OscType.TRIANGLE, 20*(2*np.pi*2*self.x)), self.y)
            #self.y = lowpass.apply(self.y, int(currentLp))
            self.y = smoother.smoothTransition(self.y)
            self.queue.put(self.y)
            self.chunk = envelope.apply(self.valueStatus.getValue(), self.y[:self.chunkSize])
            self.chunk = allpass.output(self.chunk, g1, g2, M_delay)
            self.chunk = self.chunk * self.gain
            smoother.buffer = self.y[-self.fadeSeq:]

            # frames = np.append(frames, self.chunk)
            # if len(frames) > self.chunkSize * 500:
            #     self.running = False

            self.stream.write(self.chunk.astype(np.float32).tostring())

            start = end
            end += self.chunkSize

        print("NICE")
        wavfile.write('recorded.wav', 44100, frames)
