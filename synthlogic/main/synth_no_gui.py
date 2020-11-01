import configparser
import rtmidi

from synthlogic.main.synth import Synth
from synthlogic.structures.value import DataInterface

midi_in = rtmidi.MidiIn()


def midi_info():
    print("Available MIDI ports:\n")
    available_ports = midi_in.get_ports()
    for i in range(len(available_ports)):
        print("[", i, "]", available_ports[i])
    print("\nPlease select port of a MIDI device:")


def run_synth_no_gui():
    port = None
    while not isinstance(port, int):
        midi_info()
        port = input()
        try:
            port = int(port)
        except ValueError:
            print("Port need to be a number!\n")

    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    synth = Synth()
    synth.change_midi_port(midi_in.get_port_name(port))
    data = DataInterface()
    synth.data_0interface = data
    synth.toggle()
    # basic setup
    synth.data_interface.harm_amount = int(config['HARM']['amount'])

    # no logarithm needed
    synth.data_interface.ft_cutoff.value = config['FILTER']['cutoff']
    synth.data_interface.ft_reverb.value = config['FILTER']['reverb']


    synth.data_interface.lfo_rate.value = config['LFO']['amount']
    synth.data_interface.lfo_amount.value = config['LFO']['rate']
    synth.data_interface.wf_type.value = config['OSC']['wf']

    # checked, ok!
    synth.data_interface.env_attack.value = config['ENV']['attack']
    synth.data_interface.env_decay.value = config['ENV']['decay']
    synth.data_interface.env_sustain.value = config['ENV']['sustain']
    synth.data_interface.env_release.value = config['ENV']['release']


run_synth_no_gui()