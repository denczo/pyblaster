import pyaudio
import numpy as np
import threading
import queue

from synthlogic.envelope.Envelope import Envelope
from synthlogic.filter.LowPass import LowPass
from synthlogic.filter.Allpass import Allpass
from synthlogic.oscillator import oscillator as osc
from synthlogic.structures.states.OscType import OscType
from synthlogic.oscillator.Smoother import Smoother
from synthlogic.structures.DataInterface import DataInterface


class Synth:
    def __init__(self, rate=44100, chunkSize=1024, gain=1, fadeSeq=896):

        self.data_interface = DataInterface()
        self.BUFFERSIZE = 22016
        self.writeable = self.BUFFERSIZE - chunkSize
        self.waveform = ["sine", "triangle", "sawtooth", "square"]
        self.selectedStyle = 0
        self.x = np.zeros(chunkSize+fadeSeq)
        self.t = self.x
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
        #self.osc = Oscillator()
        self.lowpass = LowPass(200)
        #g1 = 0.4
        #g2 = 0.4
        self.allpass = Allpass(self.BUFFERSIZE, self.chunkSize)
        self.envelope = Envelope(396288, self.chunkSize)
        self.smoother = Smoother(self.fadeSeq)
        self.toggle()

    def setStyle(self, val):
        self.selectedStyle = val

    def toggle(self):
        if self.running:
            print("inactive")
            self.running = False
        elif not self.running:
            print("active")
            self.running = True
            t = threading.Thread(target=self.renderNEW)
            t.start()

    def run(self):
        self.renderNEW()

    def harmonics(self, type, amount):
        #waves = int(type)
        #for i in range(waves):
        #    y = np.add(y, self.oscillator(int(freq) * (waves - i), x))
        return None

    def sum_waveforms(self, g_triangle, g_saw, g_square):
        triangle = osc.carrier(OscType.TRIANGLE, g_triangle, self.x)
        saw = osc.carrier(OscType.SAWTOOTH, g_saw, self.x)
        square = osc.carrier(OscType.SQUARE, g_square, self.x)
        return np.sum((triangle, saw, square), axis=0)

    def update_envelope(self):
        self.envelope.setAttack(self.data_interface.env_attack.value)
        self.envelope.setDecay(self.data_interface.env_decay.value)
        self.envelope.setSustain(self.data_interface.env_sustain.value)
        self.envelope.setRelease(self.data_interface.env_release.value)
        self.envelope.updateEnvelope()

    def create_samples(self, start, end):
        return np.arange(start, end + self.fadeSeq) / self.rate

    # NEW ONE
    def renderNEW(self):

        start = 0
        end = self.chunkSize
        g1 = 0.4
        g2 = 0.4

        while self.running:
            self.update_envelope()
            self.x = self.create_samples(start, end)
            fc = self.data_interface.wf_frequency.value
            fcLp = self.data_interface.ft_cutoff.value
            print(fcLp)
            self.t = osc.t(fc, self.x)

            # lfo
            lfoType = self.data_interface.lfo_type.state
            fm = self.data_interface.lfo_rate.value
            fdelta = self.data_interface.lfo_amount.value
            lfo = osc.lfo(lfoType, fm, self.x, fdelta)

            # waveform TODO simplify, write a function
            g_triangle = self.data_interface.wf_triangle.value
            g_saw = self.data_interface.wf_sawtooth.value
            g_square = self.data_interface.wf_square.value
            #print(g_triangle, g_saw, g_square)
            triangle = osc.carrier(OscType.TRIANGLE, g_triangle, self.t+lfo)
            saw = osc.carrier(OscType.SAWTOOTH, g_saw, self.t+lfo)
            square = osc.carrier(OscType.SQUARE, g_square, self.t+lfo)
            sum = np.sum((triangle, saw, square), axis=0)
            self.y = sum
            # add low pass
            self.y = self.lowpass.apply(self.y, fcLp)

            # smooth transitions between chunks
            self.y = self.smoother.smoothTransition(self.y)
            #self.y = self.lowpass.applyLfo(lfo, self.y)

            # add envelope
            pressed = self.data_interface.tp_state.state
            self.chunk = self.envelope.apply(pressed,  self.y[:self.chunkSize])

            # add reverb
            M_delay = int(self.data_interface.ft_reverb.value)
            self.chunk = self.allpass.output(self.chunk, g1, g2, M_delay)

            #self.chunk = self.chunk * self.gain
            self.queue.put(self.y)
            self.smoother.buffer = self.y[-self.fadeSeq:]

            self.stream.write(self.chunk.astype(np.float32).tostring())

            start = end
            end += self.chunkSize



    # def render(self):
    #     start = 0
    #     end = self.chunkSize
    #     g1 = 0.4
    #     g2 = 0.4
    #     allpass = Allpass(self.BUFFERSIZE, self.chunkSize)
    #     envelope = Envelope(396288, self.chunkSize)
    #     smoother = Smoother(self.fadeSeq)
    #
    #     # debug
    #     frames = np.zeros(0)
    #     lock = threading.Lock()
    #
    #     while self.running:
    #         M_delay = int(self.convert2Value(self.valueReverb.getValue(), self.writeable))
    #         #currentFreq = self.valueFrequency.getValue()
    #         currentLp = self.valueCutoff.getValue()
    #         envelope.setAttack(self.valueAttack.getValue())
    #         envelope.setDecay(self.valueDecay.getValue())
    #         envelope.setSustain(self.valueSustain.getValue())
    #         envelope.setRelease(self.valueRelease.getValue())
    #         envelope.updateEnvelope()
    #
    #         self.x = np.arange(start, end + self.fadeSeq) / self.rate
    #         #self.y = self.style(self.selectedStyle, self.x, (currentFreq+Oscillator.triangle(0.25,5, self.x)))
    #
    #         # tri = self.osc.render(OscType.TRIANGLE, currentFreq, self.x, int(self.valueTriangle.getValue())/100, typeLfo=OscType.SAWTOOTH, fm=22)
    #         # saw = self.osc.render(OscType.SAWTOOTH, currentFreq, self.x, int(self.valueSawtooth.getValue())/100, typeLfo=OscType.SAWTOOTH, fm=22)
    #         # square = self.osc.render(OscType.SQUARE, currentFreq, self.x, int(self.valueSquare.getValue())/100, typeLfo=OscType.SAWTOOTH, fm=22)
    #         # sum = np.sum((tri, saw), axis=0)
    #         # sum = np.sum((sum, square), axis=0)
    #
    #         self.y = self.renderWaveform(self.x, OscType.DEFAULT)
    #         #self.y = osc.render(OscType.SQUARE, currentFreq, self.x, int(self.valueSquare.getValue())/100)
    #         #self.y = lowpass.applyLfo(self.osc.selectWaveform(OscType.TRIANGLE, int(self.valueLfoAmount.getValue())/100*(2*np.pi*int(self.valueLfoRate.getValue())/100*self.x)), self.y)
    #         #self.y = lowpass.apply(self.y, int(currentLp))
    #         self.y = smoother.smoothTransition(self.y)
    #         self.queue.put(self.y)
    #         self.chunk = envelope.apply(self.valueStatus.getValue(), self.y[:self.chunkSize])
    #         self.chunk = allpass.output(self.chunk, g1, g2, M_delay)
    #         self.chunk = self.chunk * self.gain
    #         smoother.buffer = self.y[-self.fadeSeq:]
    #
    #         # frames = np.append(frames, self.chunk)
    #         # if len(frames) > self.chunkSize * 500:
    #         #     self.running = False
    #
    #         self.stream.write(self.chunk.astype(np.float32).tostring())
    #
    #         start = end
    #         end += self.chunkSize
    #
    #     print("NICE")
    #     wavfile.write('recorded.wav', 44100, frames)
