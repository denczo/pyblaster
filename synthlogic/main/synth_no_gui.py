import configparser

from synthlogic.main.synth import Synth
from synthlogic.structures.value import DataInterface


def run_synth_no_gui():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    synth = Synth()
    data = DataInterface()
    synth.data_interface = data
    synth.toggle()
    # basic setup
    synth.data_interface.harm_amount = int(config['HARM']['amount'])
    synth.data_interface.ft_cutoff.value = config['FILTER']['cutoff']
    synth.data_interface.ft_reverb.value = config['FILTER']['reverb']
    synth.data_interface.lfo_rate.value = config['LFO']['amount']
    synth.data_interface.lfo_amount.value = config['LFO']['rate']
    synth.data_interface.wf_frequency.value = config['OSC']['pitch']
    synth.data_interface.wf_type.value = config['OSC']['wf']

    synth.data_interface.env_attack.value = config['ENV']['attack']
    synth.data_interface.env_decay.value = config['ENV']['decay']
    synth.data_interface.env_sustain.value = config['ENV']['sustain']
    synth.data_interface.env_release.value = config['ENV']['release']


run_synth_no_gui()