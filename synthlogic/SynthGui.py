from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from synthlogic.Synth import Synth
import threading

master = Tk()
master.title("EARDRUM BLASTER")
master.resizable(width=False, height=False)
master.geometry('800x600')

synth = Synth()

def updatePlot():
    global axis, canvas

    axis.cla()
    #axis.grid()
    axis.set_yticklabels([])
    axis.set_xticklabels([])
    axis.plot(synth.x, synth.y)
    canvas.draw()
    master.after(10, updatePlot)

WIDTH_RB = 20
FIRST_COLUMN = 0
SECOND_COLUMN = FIRST_COLUMN + 1

FIRST_ROW = 0
SECOND_ROW = FIRST_ROW + 1
THIRD_ROW = SECOND_ROW + 1
FOURTH_ROW = THIRD_ROW + 1

PAD_X = 15
PAD_Y = 5

background_image = PhotoImage(file='abstract_5.gif')
#Photo by mohammad alizade on Unsplash
#Photo by Paweł Czerwiński on Unsplash
background_label = Label(image=background_image)
background_label.image = background_image
background_label.place(x=0, y=0, relwidth=1, relheight=1)
#master.configure(background='#282828')

# matplotlib
fig = Figure(figsize=(3.6, 2), facecolor='#f0f0f0')
axis = fig.add_subplot(111)

#LABELFRAME_BG = '#06266F'
#LABELFRAME_BG = '#A60000'
LABELFRAME_BG = '#444'

LABELFRAME_FG = 'white'


waveformGroup = LabelFrame(master, text="WAVEFORMS", fg=LABELFRAME_FG, bg=LABELFRAME_BG, relief=FLAT)
styleGroup = LabelFrame(master, text="STYLE", fg=LABELFRAME_FG, bg=LABELFRAME_BG, relief=FLAT)
freqGroup = LabelFrame(master, text="FREQUENCY", fg=LABELFRAME_FG, bg=LABELFRAME_BG, relief=FLAT)
envelopeGroup = LabelFrame(master, text="ENVELOPE", fg=LABELFRAME_FG, bg=LABELFRAME_BG, relief=FLAT)
filterGroup = LabelFrame(master, text="FILTER", fg=LABELFRAME_FG, bg=LABELFRAME_BG, relief=FLAT)

waveformGroup.grid(row=FIRST_ROW, column=FIRST_COLUMN, padx=PAD_X, pady=0, sticky=E+W)
styleGroup.grid(row=SECOND_ROW, column=FIRST_COLUMN, padx=PAD_X, pady=0, sticky=E+W)
freqGroup.grid(row=THIRD_ROW, column=FIRST_COLUMN, padx=PAD_X, pady=0, sticky=E+W)
envelopeGroup.grid(row=FIRST_ROW, column=SECOND_COLUMN, padx=PAD_X, pady=PAD_Y, sticky=E+W)
filterGroup.grid(row=SECOND_ROW, column=SECOND_COLUMN, padx=PAD_X, pady=PAD_Y, sticky=E+W)

frameWave = Frame(waveformGroup)
frameStyle = Frame(styleGroup)
frameFreq = Frame(freqGroup)
frameEnv = Frame(envelopeGroup)
frameFilter = Frame(filterGroup)

frameWave.grid(sticky=E+W)
frameStyle.grid(sticky=E+W)
frameFreq.grid(sticky=E+W)
frameEnv.grid(sticky=E+W)
frameFilter.grid(sticky=E+W)



canvas = FigureCanvasTkAgg(fig, master=frameFreq)
t = threading.Thread(target=updatePlot())
t.start()
#updatePlot()

group1 = StringVar()
group2 = StringVar()
group1.set(1)
group2.set(1)


# waveform options
Radiobutton(frameWave, variable=group1, text="Sine", value=1, indicatoron=0, width=WIDTH_RB, command=lambda: [synth.setWaveform(0)]).grid(row=FIRST_ROW,column=FIRST_COLUMN, padx=PAD_X, pady=PAD_Y)
Radiobutton(frameWave, variable=group1, text="Sawtooth", value=3, indicatoron=0, width=WIDTH_RB, command=lambda: [synth.setWaveform(2)]).grid(row=SECOND_ROW,column=FIRST_COLUMN, padx=PAD_X, pady=PAD_Y)
Radiobutton(frameWave, variable=group1, text="Triangle", value=2, indicatoron=0, width=WIDTH_RB, command=lambda: [synth.setWaveform(1)]).grid(row=FIRST_ROW,column=SECOND_COLUMN, padx=PAD_X, pady=PAD_Y)
Radiobutton(frameWave, variable=group1, text="Square", value=4, indicatoron=0, width=WIDTH_RB, command=lambda: [synth.setWaveform(3)]).grid(row=SECOND_ROW,column=SECOND_COLUMN, padx=PAD_X, pady=PAD_Y)

# style options
Radiobutton(frameStyle, variable=group2, text="Mono", value=1, indicatoron=0, width=WIDTH_RB, command=lambda: [synth.setStyle(1)]).grid(row=THIRD_ROW,column=FIRST_COLUMN, padx=PAD_X, pady=PAD_Y)
Radiobutton(frameStyle, variable=group2, text="Duo", value=2, indicatoron=0, width=WIDTH_RB, command=lambda: [synth.setStyle(2)]).grid(row=THIRD_ROW,column=SECOND_COLUMN, padx=PAD_X, pady=PAD_Y)
Radiobutton(frameStyle, variable=group2, text="Trio", value=3, indicatoron=0, width=WIDTH_RB, command=lambda: [synth.setStyle(3)]).grid(row=FOURTH_ROW,column=FIRST_COLUMN, padx=PAD_X, pady=PAD_Y)
Radiobutton(frameStyle, variable=group2, text="Quad", value=4, indicatoron=0, width=WIDTH_RB, command=lambda: [synth.setStyle(4)]).grid(row=FOURTH_ROW,column=SECOND_COLUMN, padx=PAD_X, pady=PAD_Y)

# frequency
canvas._tkcanvas.grid(row=FIRST_ROW, column=FIRST_COLUMN, columnspan=3)
w = Scale(frameFreq, from_=0, to=1000, length=200, orient=HORIZONTAL, resolution=1, command=lambda x: [synth.setFrequency(x)]).grid(row=SECOND_ROW, column=FIRST_COLUMN, columnspan=3, sticky=E+W, padx=PAD_X, pady=PAD_Y)
Button(frameFreq, text='Play', command=lambda: [synth.toggle()]).grid(row=THIRD_ROW, column=FIRST_COLUMN, columnspan=3, sticky=E+W, padx=PAD_X, pady=PAD_Y)

# envelope
attack = Scale(frameEnv, label="Attack",from_=100, to=0, length=100, command=synth.envGen.setAttack).grid(row=FIRST_ROW, column=FIRST_COLUMN, pady=PAD_Y)
decay = Scale(frameEnv, label="Decay",from_=100, to=0, length=100).grid(row=FIRST_ROW, column=SECOND_COLUMN, pady=PAD_Y)

# filter
reverb = Scale(frameFilter, label="Reverb", from_=synth.BUFFERSIZE, to=0, length=100, command=synth.setReverb).grid(row=FIRST_ROW, column=FIRST_COLUMN, pady=PAD_Y)
flanger = Scale(frameFilter, label="Flanger", from_=synth.BUFFERSIZE, to=0, length=100).grid(row=FIRST_ROW, column=SECOND_COLUMN, pady=PAD_Y)


mainloop()