from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from synthlogic.Synth import Synth
import threading

master = Tk()
master.title("EARDRUM BLASTER")
master.resizable(width=False, height=False)
master.geometry('468x565')

synth = Synth()


def updatePlot():
    global axis, canvas

    axis.cla()
    #axis.grid()
    axis.set_yticklabels([])
    axis.set_xticklabels([])
    axis.plot(synth.x, synth.y)
    canvas.draw()
    # every 10ms; raise, to improve performance
    master.after(10, updatePlot)


def updateBtnText():
    playBtn.configure(text=synth.status)

WIDTH_IMG = 142
WIDTH_RB = 20
HEIGHT_RB = 30
FIRST_COLUMN = 0
SECOND_COLUMN = FIRST_COLUMN + 1

FIRST_ROW = 0
SECOND_ROW = FIRST_ROW + 1
THIRD_ROW = SECOND_ROW + 1
FOURTH_ROW = THIRD_ROW + 1

PAD_X = 10
PAD_Y = 10
PAD_X_W = 5
PAD_Y_W = 5

background_image = PhotoImage(file='background.gif')
#Photo by mohammad alizade on Unsplash
#Photo by Paweł Czerwiński on Unsplash
background_label = Label(image=background_image)
background_label.image = background_image
background_label.place(x=0, y=0, relwidth=1, relheight=1)
#master.configure(background='#690008')

# matplotlib
fig = Figure(figsize=(3.2, 2), facecolor='#F0F0F0')
axis = fig.add_subplot(111)

#LABELFRAME_BG = '#053E7E'
#LABELFRAME_BG = '#A60000'
LABELFRAME_BG = '#444'
LABELFRAME_FG = 'white'

# border with label
waveformGroup = LabelFrame(master, text="WAVEFORMS", fg=LABELFRAME_FG, bg=LABELFRAME_BG, relief=FLAT)
styleGroup = LabelFrame(master, text="STYLE", fg=LABELFRAME_FG, bg=LABELFRAME_BG, relief=FLAT)
freqGroup = LabelFrame(master, text="FREQUENCY", fg=LABELFRAME_FG, bg=LABELFRAME_BG, relief=FLAT)
envelopeGroup = LabelFrame(master, text="ENVELOPE", fg=LABELFRAME_FG, bg=LABELFRAME_BG, relief=FLAT)
filterGroup = LabelFrame(master, text="FILTER", fg=LABELFRAME_FG, bg=LABELFRAME_BG, relief=FLAT)

# group of widgets
waveformGroup.grid(row=FIRST_ROW, column=FIRST_COLUMN, rowspan=1, padx=PAD_X, pady=PAD_Y, sticky=N+E+W)
styleGroup.grid(row=SECOND_ROW, column=FIRST_COLUMN, rowspan=1, padx=PAD_X, pady=(0, PAD_Y), sticky=N+E+W)
freqGroup.grid(row=THIRD_ROW, column=FIRST_COLUMN, rowspan=1, padx=PAD_X, pady=(0, PAD_Y), sticky=N+E+W)
envelopeGroup.grid(row=FIRST_ROW, column=SECOND_COLUMN, rowspan=2, padx=(0, PAD_X), pady=PAD_Y, sticky=N+E+W)
filterGroup.grid(row=THIRD_ROW, column=SECOND_COLUMN, rowspan=2, padx=(0, PAD_X), pady=(0, PAD_Y), sticky=N+E+W)

# gray inner box
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

# default selection
group1 = StringVar()
group2 = StringVar()
group1.set(1)
group2.set(1)

sineIcon = PhotoImage(file="icons/sine.png")
triangleIcon = PhotoImage(file="icons/triangle.png")
sawtoothIcon = PhotoImage(file="icons/sawtooth.png")
squareIcon = PhotoImage(file="icons/square.png")

# waveform options
rSine = Radiobutton(frameWave, image=sineIcon, variable=group1, value=1, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setWaveform(0)]).grid(row=FIRST_ROW, column=FIRST_COLUMN, padx=PAD_X_W, pady=(PAD_Y_W, 0))
rSaw = Radiobutton(frameWave, image=sawtoothIcon, variable=group1, value=3, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setWaveform(2)]).grid(row=SECOND_ROW, column=FIRST_COLUMN, padx=PAD_X_W, pady=PAD_Y_W)
rTriangle = Radiobutton(frameWave, image=triangleIcon, variable=group1, value=2, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setWaveform(1)]).grid(row=FIRST_ROW, column=SECOND_COLUMN, padx=PAD_X_W, pady=(PAD_Y_W, 0))
rSquare = Radiobutton(frameWave, image=squareIcon, variable=group1, value=4, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setWaveform(3)]).grid(row=SECOND_ROW, column=SECOND_COLUMN, padx=PAD_X_W, pady=PAD_Y_W)

monoIcon = PhotoImage(file="icons/mono.png")
duoIcon = PhotoImage(file="icons/duo.png")
trioIcon = PhotoImage(file="icons/trio.png")
quattroIcon = PhotoImage(file="icons/quattro.png")

# style options
Radiobutton(frameStyle, variable=group2, image=monoIcon, value=1, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setStyle(1)]).grid(row=THIRD_ROW,column=FIRST_COLUMN, padx=PAD_X_W, pady=(PAD_Y_W, 0))
Radiobutton(frameStyle, variable=group2, image=duoIcon, value=2, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setStyle(2)]).grid(row=THIRD_ROW,column=SECOND_COLUMN, padx=PAD_X_W, pady=(PAD_Y_W, 0))
Radiobutton(frameStyle, variable=group2, image=trioIcon, value=3, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setStyle(3)]).grid(row=FOURTH_ROW,column=FIRST_COLUMN, padx=PAD_X_W, pady=PAD_Y_W)
Radiobutton(frameStyle, variable=group2, image=quattroIcon, value=4, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setStyle(4)]).grid(row=FOURTH_ROW,column=SECOND_COLUMN, padx=PAD_X_W, pady=PAD_Y_W)

# frequency
canvas._tkcanvas.grid(row=FIRST_ROW, column=FIRST_COLUMN, columnspan=3)
w = Scale(frameFreq, from_=0, to=1000, length=200, orient=HORIZONTAL, resolution=1, command=lambda x: [synth.setFrequency(x)]).grid(row=SECOND_ROW, column=FIRST_COLUMN, columnspan=3, sticky=E+W, padx=PAD_X_W, pady=PAD_Y_W)
playBtn = Button(frameFreq, text=synth.status, command=lambda: [synth.toggle(), updateBtnText()])
playBtn.grid(row=THIRD_ROW, column=FIRST_COLUMN, columnspan=3, sticky=E+W, padx=PAD_X_W, pady=PAD_Y_W)

# envelope
attack = Scale(frameEnv, from_=100, to=0, length=100, command=synth.envGen.setAttack).grid(row=FIRST_ROW, column=FIRST_COLUMN, padx=PAD_X_W, pady=PAD_Y_W)
decay = Scale(frameEnv, from_=100, to=0, length=100).grid(row=FIRST_ROW, column=SECOND_COLUMN, padx=PAD_X_W, pady=PAD_Y_W)
attackLabel = Label(frameEnv, text="Attack").grid(row=SECOND_ROW, column=FIRST_COLUMN)
decayLabel = Label(frameEnv, text="Decay").grid(row=SECOND_ROW, column=SECOND_COLUMN)

# filter
reverb = Scale(frameFilter, from_=100, to=0, length=100, command=synth.setReverb).grid(row=FIRST_ROW, column=FIRST_COLUMN, padx=PAD_X_W, pady=PAD_Y_W)
flanger = Scale(frameFilter, from_=100, to=0, length=100).grid(row=FIRST_ROW, column=SECOND_COLUMN, padx=PAD_X_W, pady=PAD_Y_W)
reverbLabel = Label(frameFilter, text="Reverb").grid(row=SECOND_ROW, column=FIRST_COLUMN)
flangerLabel = Label(frameFilter, text="Flanger").grid(row=SECOND_ROW, column=SECOND_COLUMN)

mainloop()
