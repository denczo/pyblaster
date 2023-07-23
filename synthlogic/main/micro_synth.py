import pyaudio
import numpy as np
import threading
import sys

sys.path.append("/home/pi/synth")
from interfaces.ext_input.midi import MidiInterface
from processing.envelope import Env
import processing.oscillator as osc
from structures.value import DataInterface


class Synth:
    def __init__(self, rate=44100, chunk_size=1024, gain=0.25, fade_seq=256):

        self.midi_port = None
        self.midi_interface = None
        self.rate = int(rate)
        self.chunk_size = chunk_size
        self.p = pyaudio.PyAudio()
        self.stream = self.settings(1, self.rate, 1, self.chunk_size)
        self.stream.start_stream()

        self.waveform = ["triangle", "sawtooth", "square"]
        self.x = np.zeros(chunk_size + fade_seq)
        self.t = self.x
        self.y = np.zeros(chunk_size + fade_seq)
        self.chunk = np.zeros(chunk_size)
        self.gain = gain
        self.fade_seq = fade_seq

        self.data_interface = DataInterface()
        self.running = False
        self.pressed = False

        self.smoother = osc.Smoother(self.fade_seq)
        self.env = Env(0, 0, 0, 0, gain)

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

        while self.running:

            pressedKp = False
            if self.midi_interface is not None:
                pressedKp = self.data_interface.kb_state.state

            pressed = False

            if pressedKp and self.midi_interface is not None:
                currentFreq = self.midi_interface.currentFreq
                pressed = pressedKp

            fc = currentFreq
            self.env.settings(self.data_interface.env_attack.value,
                              self.data_interface.env_decay.value,
                              self.data_interface.env_sustain.value,
                              self.data_interface.env_release.value,
                              self.gain)

            self.x = self.create_samples(start, end)

            wf = self.gain * osc.carrier(self.data_interface.wf_type.state, fc, self.x)
            self.y = osc.harmonics(self.data_interface.wf_type.state, wf, fc, self.x, self.data_interface.harm_amount,
                                   0)

            self.y *= self.env.apply(pressed)
            self.y = self.smoother.smoothTransition(self.y)
            self.chunk = self.y[:self.chunk_size]

            self.smoother.buffer = self.y[-self.fade_seq:]
            self.stream.write(self.chunk.astype(np.float32).tostring())

            start = end
            end += self.chunk_size
