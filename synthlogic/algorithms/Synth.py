import pyaudio
import numpy as np
import threading
import queue

from synthlogic.envelope.Envelope import Envelope
from synthlogic.filter.LowPass import LowPass
from synthlogic.filter.Allpass import Allpass
from synthlogic.midi.MidiInterface import MidiInterface
from synthlogic.oscillator import oscillator as osc
from synthlogic.oscillator.LfoMode import LfoMode
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

    def harmonics(self, type_wf, g, fc, amount, lfo):
        t = osc.t(fc, self.x)
        y = osc.carrier(type_wf, g, t+lfo)
        start = 2
        for i in range(start, amount+start):
            t = osc.t(fc*i, self.x)
            y = np.add(y, osc.carrier(type_wf, g, t+lfo))
        return y

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
        midi_interface = MidiInterface(0, self.data_interface)
        midi_interface.midi_in.set_callback(midi_interface)

        while self.running:
            self.update_envelope()
            self.x = self.create_samples(start, end)

            pressedTp = self.data_interface.tp_state.state
            pressedKb = midi_interface.data.tp_state.state
            pressed = False
            fc = 0

            if not pressedKb:
                pressed = pressedTp
                fc = self.data_interface.wf_frequency.value
            elif not pressedTp:
                pressed = pressedKb
                fc = midi_interface.currentFreq

            #fc = self.data_interface.wf_frequency.value
            #fc = midi_interface.currentFreq
            fcLp = self.data_interface.ft_cutoff.value
            #print(fcLp)
            self.t = osc.t(fc, self.x)

            # lfo
            lfoMode = self.data_interface.lfo_mode.state
            lfoType = self.data_interface.lfo_type.state
            fm = self.data_interface.lfo_rate.value
            fdelta = self.data_interface.lfo_amount.value
            lfo = osc.lfo(lfoType, fm, self.x, fdelta)
            lfo_default = 0
            lfo_filter = 0
            if lfoMode == LfoMode.DEFAULT.value:
                lfo_default = lfo
            else:
                lfo_filter = lfo

            # waveform TODO simplify, write a function
            g_triangle = self.data_interface.wf_triangle.value
            g_saw = self.data_interface.wf_sawtooth.value
            g_square = self.data_interface.wf_square.value

            triangle = self.harmonics(OscType.TRIANGLE.value, g_triangle, fc, self.data_interface.harm_amount, lfo_default)
            saw = self.harmonics(OscType.SAWTOOTH.value, g_saw, fc, self.data_interface.harm_amount, lfo_default)
            square = self.harmonics(OscType.SQUARE.value, g_square, fc, self.data_interface.harm_amount, lfo_default)

            sum = np.sum((triangle, saw, square), axis=0)
            self.y = sum
            # add low pass
            self.y = self.lowpass.apply(self.y, fcLp)
            self.y = self.lowpass.applyLfo(lfo_filter, self.y)

            # smooth transitions between chunks
            self.y = self.smoother.smoothTransition(self.y)

            # add envelope
            # pressedTp = self.data_interface.tp_state.state
            # pressedKb = midi_interface.data.tp_state.state
            #
            # if not pressedKb:
            #     pressed = pressedTp
            # elif not pressedTp:
            #     pressed = pressedKb

            #print(pressed)
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
