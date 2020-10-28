# EARDRUM BLASTER
### Digital Synthesizer in Python

##### How to use

run with gui: `python3 synth_gui.py`\
___
run without gui: `python3 synth_no_gui.py`\

change settings of synth in `config.ini`
___


##### Components
- Pyaudio
- tkinter
- Python 3
- python-rtMidi
- Scipy

##### Features
- 3 Waveforms 
    - Triangle, Sawtooth, Rectangular
- 4 Phase Envelope 
    - Attack, Decay, Sustain, Release
- Filter: Low-Pass, Reverb
- Midi 
- LFO (to controll pitch or low-pass)

##### Planned features
- remove library Scipy and replace waveform synthesis with own implementation
- paraphonic
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
