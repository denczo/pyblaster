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
    def __init__(self, rate=44100, chunkSize=1024, gain=1, fadeSeq=896):

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
        self.osc = Oscillator()
        self.lowpass = LowPass(200)

        # setter; tkinter needs objects to pass commands as parameter
        # values for waveforms
        maxFreq = float(5000)
        maxVal = float(1)
        self.valueSawtooth = ValueCarrier(maxVal)
        self.valueTriangle = ValueCarrier(maxVal)
        self.valueSquare = ValueCarrier(maxVal)

        # values for effects
        self.valueReverb = ValueCarrier(maxVal)
        self.valueCutoff = ValueCarrier(maxVal)
        self.valueFlanger = ValueCarrier(maxVal)
        self.valueDelay = ValueCarrier(maxVal)

        # values of envelope
        self.valueAttack = ValueCarrier(maxVal)
        self.valueDecay = ValueCarrier(maxVal)
        self.valueSustain = ValueCarrier(maxVal)
        self.valueRelease = ValueCarrier(maxVal)

        # values of lfo
        self.valueLfoRate = ValueCarrier(20)
        self.valueLfoAmount = ValueCarrier(1)
        self.valueLfoType = ValueCarrier(3)

        self.valueStyle = ValueCarrier(4)
        self.valueFrequency = ValueCarrier(5000)
        self.valueStatus = ValueCarrier(100)

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

    def renderWaveform(self, x, lfoType):

        #LFO none
        currentFreq = self.valueFrequency.getValue()
        fm = self.valueLfoRate.getValue()
        lfo = self.osc.lfo(lfoType, fm, x)
        t = self.osc.t(currentFreq, x)

        triangle = self.osc.carrier(OscType.TRIANGLE, t, self.valueTriangle.getValue(), lfo)
        saw = self.osc.carrier(OscType.SAWTOOTH, t, self.valueSawtooth.getValue(), lfo)
        square = self.osc.carrier(OscType.SQUARE, t, self.valueTriangle.getValue(), lfo)
        return np.sum((triangle, saw, square), axis=0)

        #triangle = self.osc.render(OscType.TRIANGLE, currentFreq, self.x, self.valueTriangle.getValue(), typeLfo=lfoType, fm=fm)
        #saw = self.osc.render(OscType.SAWTOOTH, currentFreq, self.x, self.valueSawtooth.getValue(), typeLfo=lfoType, fm=fm)
        #square = self.osc.render(OscType.SQUARE, currentFreq, self.x, self.valueSquare.getValue(), typeLfo=lfoType, fm=fm)
        #sum = np.sum((triangle, saw), axis=0)
        #sum = np.sum((sum, square), axis=0)

    def renderLfoFilter(self, value):
        amount = self.valueLfoAmount.getValue()
        rate = self.valueLfoRate.getValue()
        lfo = self.osc.selectWaveform(value, amount * 2 * np.pi * rate * self.x)
        return self.lowpass.applyLfo(lfo, self.y)

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

            # tri = self.osc.render(OscType.TRIANGLE, currentFreq, self.x, int(self.valueTriangle.getValue())/100, typeLfo=OscType.SAWTOOTH, fm=22)
            # saw = self.osc.render(OscType.SAWTOOTH, currentFreq, self.x, int(self.valueSawtooth.getValue())/100, typeLfo=OscType.SAWTOOTH, fm=22)
            # square = self.osc.render(OscType.SQUARE, currentFreq, self.x, int(self.valueSquare.getValue())/100, typeLfo=OscType.SAWTOOTH, fm=22)
            # sum = np.sum((tri, saw), axis=0)
            # sum = np.sum((sum, square), axis=0)
            self.y = self.renderWaveform(self.x, OscType.SQUARE)
            #self.y = osc.render(OscType.SQUARE, currentFreq, self.x, int(self.valueSquare.getValue())/100)
            #self.y = lowpass.applyLfo(self.osc.selectWaveform(OscType.TRIANGLE, int(self.valueLfoAmount.getValue())/100*(2*np.pi*int(self.valueLfoRate.getValue())/100*self.x)), self.y)
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
