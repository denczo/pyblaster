# EARDRUM BLASTER
### Digital Synthesizer in Python

##### How to use

install all required libraries (listed under components)

run with gui: `python3 /synthlogic/main/synth_gui.py`

*OR*
 
run without gui: `python3 /synthlogic/main/synth_no_gui.py`

change settings of synth in `config.ini`
___

##### How to install on Raspberry Pi
running the synthesizer on your Raspberry Pi is currently experimental.
It will run but it's not optimized for it. It was testet on a *Raspberry Pi 2 B*.
For those who still want to try it out, here is a tutorial how to install it:
http://denicz.info/2020/11/04/how-to-install-eardrum-blaster-on-raspberry-pi/

___

##### Components
- Pyaudio
- tkinter
- Python 3
- python-rtMidi
- Scipy
- numpy

##### Features
- 3 Waveforms 
    - Triangle, Sawtooth, Rectangular
- 4 Phase Envelope 
    - Attack, Decay, Sustain, Release
- Filter: Low-Pass, Reverb
- Midi-In
- LFO (to controll pitch or low-pass)
- version with GUI and version which can be run from console

##### Planned features
- remove library Scipy and replace waveform synthesis with own implementation
- paraphony
- optimize performance on Raspberry Pi
___
##### Learn more about DSP and Pyaudio

- similar project
    - https://github.com/Kurene/simple-synthesizer-with-pyqt5-pyaudio/blob/master/main.py
- basics
    - https://www.mathsisfun.com/algebra/amplitude-period-frequency-phase-shift.html
    - http://www.dspguide.com/pdfbook.htm
- smoothing
    - http://www.fon.hum.uva.nl/praat/manual/Sounds__Concatenate_with_overlap___.html
- filter
    - https://ccrma.stanford.edu/~jos/pasp/Comb_Filters.html
    - https://ccrma.stanford.edu/~jos/pasp/Delay_Lines.html
    - https://medium.com/the-seekers-project/coding-a-basic-reverb-algorithm-an-introduction-to-audio-programming-d5d90ad58bde
