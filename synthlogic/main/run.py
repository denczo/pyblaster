import configparser

import pyaudio
import numpy as np
import threading
import queue
import sys

sys.path.append("/home/pi/synth")
from synthlogic.interfaces.ext_input.midi import MidiInterface
from synthlogic.processing.envelope import Envelope
from synthlogic.processing.filter import LowPass, Allpass
import synthlogic.processing.oscillator as osc
from synthlogic.structures.value import DataInterface, OscType, LfoMode



class Synth:
    def __init__(self, rate=44100, chunk_size=1024, gain=1, fade_seq=896):

        self.rate = int(rate)
        self.chunk_size = chunk_size
        self.p = pyaudio.PyAudio()
        self.stream = self.settings(1, self.rate, 1, self.chunk_size)
        self.stream.start_stream()

        self.BUFFERSIZE = 22016
        self.writeable = self.BUFFERSIZE - chunk_size
        self.waveform = ["sine", "triangle", "sawtooth", "square"]
        self.x = np.zeros(chunk_size + fade_seq)
        self.t = self.x
        self.y = np.zeros(chunk_size + fade_seq)
        self.chunk = np.zeros(chunk_size)
        self.gain = gain
        self.fade_seq = fade_seq
        # self.queue = queue.LifoQueue()

        self.data_interface = DataInterface()
        self.running = False
        self.pressed = False
        #self.lowpass = LowPass(200)
        # g1 = 0.4
        # g2 = 0.4
        self.allpass = Allpass(self.BUFFERSIZE, self.chunk_size)
        #self.envelope = Envelope(396288, self.chunk_size)
        self.smoother = osc.Smoother(self.fade_seq)
        self.toggle()
        #self.penis()

    def settings(self, channels, rate, output, chunk_size):
        return self.p.open(format=pyaudio.paFloat32,
                           channels=channels,
                           rate=rate,
                           output=output,
                           frames_per_buffer=chunk_size)

    def penis(self):
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            print((i, dev['name'], dev['maxInputChannels']), dev['defaultSampleRate'])

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

    def harmonics(self, type_wf, g, fc, amount, lfo):
        t = osc.t(fc, self.x)
        y = osc.carrier(type_wf, g, t + lfo)
        start = 2
        for i in range(start, amount + start):
            t = osc.t(fc * i, self.x)
            y = np.add(y, osc.carrier(type_wf, g, t + lfo))
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
        return np.arange(start, end + self.fade_seq) / self.rate

    def render(self):

        start = 0
        end = self.chunk_size
        midi_interface = MidiInterface(1, self.data_interface)
        midi_interface.midi_in.set_callback(midi_interface)
        currentFreq = 0
        g1 = 0.4
        g2 = 0.4

        while self.running:

            pressedKb = midi_interface.data.tp_state.state
            if pressedKb:
                currentFreq = midi_interface.currentFreq
            else:
                currentFreq = 0

            self.x = self.create_samples(start, end)
            fc = currentFreq
            self.t = osc.t(fc, self.x)
            triangle = osc.carrier(OscType.SAWTOOTH, 0.99, self.t)
            self.y = triangle
            self.chunk = self.y[:self.chunk_size] * self.gain
            self.y = self.smoother.smoothTransition(self.y)

            # add reverb
            M_delay = int(self.data_interface.ft_reverb.value)
            self.chunk = self.allpass.output(self.chunk, g1, g2, M_delay)

            self.smoother.buffer = self.y[-self.fade_seq:]
            self.stream.write(self.chunk.astype(np.float32).tostring())
            start = end
            end += self.chunk_size



            # # lfo
            # # waveform TODO simplify, write a function
            #g_triangle = self.data_interface.wf_triangle.value
            #g_saw = self.data_interface.wf_sawtooth.value
            #g_square = self.data_interface.wf_square.value
            #
            # # triangle = self.harmonics(OscType.TRIANGLE.value, g_triangle, fc, self.data_interface.harm_amount, lfo_default)
            # saw = self.harmonics(OscType.SAWTOOTH.value, g_saw, fc, self.data_interface.harm_amount, lfo_default)
            # # square = self.harmonics(OscType.SQUARE.value, g_square, fc, self.data_interface.harm_amount, lfo_default)
            #
            # # sum = np.sum((triangle, saw, square), axis=0)
            # self.y = saw
            # # add low pass
            # # self.y = self.lowpass.apply(self.y, fcLp)
            # # self.y = self.lowpass.applyLfo(lfo_filter, self.y)
            #
            # # smooth transitions between chunks
            # self.y = self.smoother.smoothTransition(self.y)
            #
            # # add envelope
            # # pressedTp = self.data_interface.tp_state.state
            # # pressedKb = midi_interface.data.tp_state.state
            # #
            # # if not pressedKb:
            # #     pressed = pressedTp
            # # elif not pressedTp:
            # #     pressed = pressedKb
            #
            # # print(pressed)
            # # self.chunk = self.envelope.apply(pressed,  self.y[:self.chunkSize])
            #
            # # add reverb
            # M_delay = int(self.data_interface.ft_reverb.value)
            # # self.chunk = self.allpass.output(self.chunk, g1, g2, M_delay)
            # self.chunk = self.y
            #
            # # self.chunk = self.chunk * self.gain
            # # self.queue.put(self.y)
            # self.smoother.buffer = self.y[-self.fadeSeq:]
            #
            # self.stream.write(self.chunk.astype(np.float32).tostring())
            #
            # start = end
            # end += self.chunkSize


def run_synth_no_gui():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    synth = Synth()
    data = DataInterface()
    synth.data_interface = data
    # basic setup
    synth.data_interface.harm_amount = int(config['HARM']['amount'])
    synth.data_interface.ft_cutoff.value = config['FILTER']['cutoff']
    synth.data_interface.ft_reverb.value = config['FILTER']['reverb']
    synth.data_interface.lfo_rate.value = config['LFO']['amount']
    synth.data_interface.lfo_amount.value = config['LFO']['rate']
    synth.data_interface.wf_frequency.value = config['OSC']['pitch']
    synth.data_interface.wf_triangle.value = config['OSC']['triangle']
    synth.data_interface.wf_sawtooth.value = config['OSC']['sawtooth']
    synth.data_interface.wf_square.value = config['OSC']['rectangular']
    synth.data_interface.env_attack.value = config['ENV']['attack']
    synth.data_interface.env_decay.value = config['ENV']['decay']
    synth.data_interface.env_sustain.value = config['ENV']['sustain']
    synth.data_interface.env_release.value = config['ENV']['release']


def run_synth_gui():
    pass


run_synth_no_gui()
