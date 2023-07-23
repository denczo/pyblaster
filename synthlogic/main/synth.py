
import pyaudio
import numpy as np
import threading
import queue
import sys
from scipy.io import wavfile

sys.path.append("/home/pi/synth")
from interfaces.ext_input.midi import MidiInterface
from processing.envelope import Env
from processing.filter import LowPass, Allpass
import processing.oscillator as osc
from structures.value import DataInterface


class Synth:
    def __init__(self, rate=44100, chunk_size=1024, gain=0.25, fade_seq=0, gui_enabled=False):

        self.midi_port = None
        self.midi_interface = None
        self.rate = int(rate)
        self.chunk_size = chunk_size
        self.p = pyaudio.PyAudio()
        self.stream = self.settings(1, self.rate, 1, self.chunk_size)
        self.stream.start_stream()
        self.gui_enabled = gui_enabled

        self.BUFFERSIZE = 22016
        self.writeable = self.BUFFERSIZE - chunk_size
        self.waveform = ["triangle", "sawtooth", "square"]
        self.x = np.zeros(chunk_size + fade_seq)
        self.t = self.x
        self.y = np.zeros(chunk_size + fade_seq)
        self.chunk = np.zeros(chunk_size)
        self.gain = gain
        self.fade_seq = fade_seq
        self.queue = queue.LifoQueue()

        self.data_interface = DataInterface()
        self.running = False
        self.pressed = False

        self.lowpass = LowPass(200)
        self.allpass = Allpass(self.BUFFERSIZE, self.chunk_size)
        self.smoother = osc.Smoother(self.fade_seq)
        self.env = Env(0, 0, 0, 0, gain)
        self.lfo = np.zeros(chunk_size)

    def settings(self, channels, rate, output, chunk_size):
        return self.p.open(format=pyaudio.paFloat32,
                           channels=channels,
                           rate=rate,
                           output=output,
                           frames_per_buffer=chunk_size)

    def devices(self):
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

    def create_samples(self, start, end):
        return np.arange(start, end + self.fade_seq) / self.rate

    def change_midi_port(self, port, port_count):
        print("midi port changed to:", port)
        if port is not None and port < port_count:
            self.midi_interface = None
            self.midi_interface = MidiInterface(int(port), self.data_interface)
            self.midi_interface.midi_in.set_callback(self.midi_interface)
        else:
            self.midi_interface = None

    def render(self):

        start = 0
        end = self.chunk_size
        currentFreq = 0
        g1 = 0.4
        g2 = 0.4
        chunks = []

        while self.running:

            pressedKp = False
            if self.midi_interface is not None:
                pressedKp = self.data_interface.kb_state.state

            pressedTp = self.data_interface.tp_state.state
            pressed = False

            if pressedTp:
                currentFreq = self.data_interface.wf_frequency.value_log
                pressed = pressedTp
            elif pressedKp and self.midi_interface is not None:
                currentFreq = self.midi_interface.currentFreq
                pressed = pressedKp

            fc = currentFreq
            if self.gui_enabled:
                fc_Lp = self.data_interface.ft_cutoff.value_log
                M_delay = int(self.data_interface.ft_reverb.value_log)
                self.env.settings(self.data_interface.env_attack.value_log,
                                  self.data_interface.env_decay.value_log,
                                  self.data_interface.env_sustain.value_log,
                                  self.data_interface.env_release.value_log,
                                  self.gain)
            else:
                fc_Lp = self.data_interface.ft_cutoff.value
                M_delay = int(self.data_interface.ft_reverb.value)
                self.env.settings(self.data_interface.env_attack.value,
                                  self.data_interface.env_decay.value,
                                  self.data_interface.env_sustain.value,
                                  self.data_interface.env_release.value,
                                  self.gain)

            self.x = self.create_samples(start, end)

            # lfo
            lfoType = self.data_interface.lfo_type.state
            fm = self.data_interface.lfo_rate.value_log
            fdelta = self.data_interface.lfo_amount.value_log
            #fdelta = 50
            self.lfo = osc.lfo(lfoType, fm, self.x, self.lfo[-1], fdelta)

            wf = self.gain*osc.carrier(self.data_interface.wf_type.state, fc, self.x, self.lfo)
            self.y = osc.harmonics(self.data_interface.wf_type.state, wf, fc, self.x, self.data_interface.harm_amount, self.lfo)
            #self.y = wf
            #self.y *= self.lowpass.calcBlackmanWindow(self.chunk_size)
            #self.y = self.lowpass.apply(self.y, fc_Lp)
            #self.y = self.lowpass.applyLfo(self.lfo, self.y)
            self.y *= self.env.apply(pressed)
            #self.y = self.smoother.smoothTransition(self.y)
            self.chunk = self.y[:self.chunk_size]

            self.chunk = self.allpass.output(self.y[:self.chunk_size], g1, g2, M_delay)

            # for visualisation
            self.queue.put(self.chunk)
            #self.smoother.buffer = self.y1[-self.fade_seq:]
            self.stream.write(self.chunk.astype(np.float32).tostring())

            start = end
            end += self.chunk_size

        #     chunks = np.append(chunks, self.chunk)
        #     if start >= 441000:
        #        self.toggle()
        #
        # print('ended')
        # wavfile.write('recorded.wav', 44100, chunks)