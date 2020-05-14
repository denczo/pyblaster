from tkinter import *
from tkinter import messagebox

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from synthlogic.algorithms.Synth import Synth
import threading
from PIL import Image, ImageTk


from synthlogic.gui.Section import Section
from synthlogic.gui.button.ButtonGroup import ButtonGroup
from synthlogic.gui.Touchpad import Touchpad
from synthlogic.gui.slider.SliderGroup import SliderGroup

# === basic window configuration
from synthlogic.gui.slider.EffectPair import EffectPair

master = Tk()
master.title("EARDRUM BLASTER")
master.resizable(width=False, height=False)
winWidth = 558
winHeight = 650
windowSize = str(winHeight)+'x'+str(winHeight)
# window spawn in center of screen
screenWidth = master.winfo_screenwidth()
screenHeight = master.winfo_screenheight()
startX = int((screenWidth/2) - (winWidth/2))
startY = int((screenHeight/2) - (winHeight/2))
master.geometry('{}x{}+{}+{}'.format(winWidth, winHeight, startX, startY))
# synthesizer
synth = Synth()
x = np.arange(0, 1024)

def updatePlot():
    global axis, canvas
    axis.cla()
    axis.set_xticks([], [])
    axis.set_yticks([], [])
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.spines['left'].set_visible(False)
    bla = synth.queue.get()
    axis.plot(x, bla[:1024])
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9)

    canvas.draw()
    # every 10ms; raise, to improve performance
    master.after(50, updatePlot)

def on_close():
    # custom close options, here's one example:

    close = messagebox.askokcancel("Close", "Would you like to close the EARDRUM BLASTER?")
    if close:
        synth.running = False
        master.destroy()

master.protocol("WM_DELETE_WINDOW", on_close)



WIDTH_IMG = 50
WIDTH_RB = WIDTH_IMG
HEIGHT_RB = WIDTH_RB

FIRST = 0
SECOND = FIRST + 1
THIRD = SECOND + 1
FOURTH = THIRD + 1
FIFTH = FOURTH + 1
SIXTH = FIFTH + 1
SEVENTH = SIXTH + 1
EIGHTH = SEVENTH + 1

PAD_X = 10
PAD_Y = 10
PAD_X_W = 5
PAD_Y_W = 5

background_image = ImageTk.PhotoImage(file='../icons/background/scratch.jpg')
touchpad_bg = PhotoImage(file='../icons/touchpad/touchpad.gif')

#Photo by mohammad alizade on Unsplash
#Photo by Paweł Czerwiński on Unsplash
background_label = Label(image=background_image)
background_label.image = background_image
background_label.place(x=0, y=0, relwidth=1, relheight=1)
master.configure(background='#CFB53B')

LABELFRAME_BG = '#444'
LABELFRAME_FG = 'white'

# default selection
group = StringVar()
group.set(1)

sineIcon = PhotoImage(file="../icons/waveforms/Sine.png")
triangleIcon = PhotoImage(file="../icons/waveforms/Triangle.png")
sawtoothIcon = PhotoImage(file="../icons/waveforms/Sawtooth.png")
squareIcon = PhotoImage(file="../icons/waveforms/Square.png")

# === oscillator section
sectionOsc = Section(master, "OSCILLATOR", LABELFRAME_FG, LABELFRAME_BG)
sectionOsc.setPosition(FIRST, FIRST, 2, 1, PAD_X, PAD_Y)
oscillator = SliderGroup(sectionOsc.getSection())
oscillator.create(["Pitch", triangleIcon, sawtoothIcon, squareIcon],
                  [synth.valueFrequency, synth.valueTriangle, synth.valueSawtooth, synth.valueSquare])

# === style options
monoIcon = PhotoImage(file="../icons/style/mono.png")
duoIcon = PhotoImage(file="../icons/style/duo.png")
trioIcon = PhotoImage(file="../icons/style/trio.png")
quattroIcon = PhotoImage(file="../icons/style/quattro.png")

sectionStyle = Section(master, "STYLE", LABELFRAME_FG, LABELFRAME_BG)
sectionStyle.setPosition(THIRD, FIRST, 1, 1, PAD_X, (0, PAD_Y))
Radiobutton(sectionStyle.getSection(), variable=group, image=monoIcon, value=1, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setStyle(1)]).grid(row=FIRST,column=FIRST, padx=(6,0), pady=(PAD_Y_W, 0))
Radiobutton(sectionStyle.getSection(), variable=group, image=duoIcon, value=2, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setStyle(2)]).grid(row=FIRST,column=SECOND, padx=(5,0), pady=(PAD_Y_W, 0))
Radiobutton(sectionStyle.getSection(), variable=group, image=trioIcon, value=3, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setStyle(3)]).grid(row=FIRST,column=THIRD, padx=(5,0), pady=PAD_Y_W)
Radiobutton(sectionStyle.getSection(), variable=group, image=quattroIcon, value=4, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setStyle(4)]).grid(row=FIRST,column=FOURTH, padx=(5,7), pady=PAD_Y_W)

# === chunk section
sectionChunk = Section(master, "CHUNK", LABELFRAME_FG, LABELFRAME_BG)
sectionChunk.setPosition(FOURTH, FIRST, 1, 1, PAD_X, (0, PAD_Y))
fig = Figure(figsize=(2.6, 1), facecolor='#F0F0F0')
axis = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=sectionChunk.getSection())
canvas._tkcanvas.grid(row=FIRST, column=FIRST, sticky=E+W)
t = threading.Thread(target=updatePlot())
t.start()

# === touchpad section
sectionTouchpad = Section(master, "TOUCH ME", LABELFRAME_FG, LABELFRAME_BG)
sectionTouchpad.setPosition(FIFTH, FIRST, 2, 1, PAD_X, (0, PAD_Y))
touchpad = Touchpad(sectionTouchpad.getSection(), 260, 195, synth)

# === envelope section
sectionEnv = Section(master, "ENVELOPE", LABELFRAME_FG, LABELFRAME_BG)
sectionEnv.setPosition(FIRST, SECOND, 1, 1, (0, PAD_X), PAD_Y)
effects = SliderGroup(sectionEnv.getSection())
effects.create(["Attack", "Decay", "Sustain", "Release"],
               [synth.valueAttack, synth.valueDecay, synth.valueSustain, synth.valueRelease])

# === filter section
sectionFilter = Section(master, "FILTER", LABELFRAME_FG, LABELFRAME_BG)
sectionFilter.setPosition(THIRD, SECOND, 2, 2, (0, PAD_X), 0)
effects = SliderGroup(sectionFilter.getSection())
effects.create(["Reverb", "Cutoff"], [synth.valueReverb, synth.valueCutoff])

# === lfo options

tri = Image.open("../icons/waveforms/Triangle.png")
tri = tri.resize((20, 20), Image.ANTIALIAS)
triR = ImageTk.PhotoImage(tri)
saw = Image.open("../icons/waveforms/Sawtooth.png")
saw = saw.resize((20, 20), Image.ANTIALIAS)
sawR = ImageTk.PhotoImage(saw)
sqare = Image.open("../icons/waveforms/Square.png")
sqare = sqare.resize((20, 20), Image.ANTIALIAS)
sqareR = ImageTk.PhotoImage(sqare)

WIDTH_IMG = 20
HEIGHT_RB = 20

sectionLFO = Section(master, "LFO", LABELFRAME_FG, LABELFRAME_BG)
sectionLFO.setPosition(FIFTH, SECOND, 1, 1, (0, PAD_X), (0, PAD_Y))
lfoType = ButtonGroup(sectionLFO.getSection(), startColumn=2)
lfoType.create([triR, sawR, sqareR], width=WIDTH_IMG, height=HEIGHT_RB, variable="type")
lfoType.posVertical(padx=5, pady=15, gap=30)

lfoStyle = ButtonGroup(sectionLFO.getSection(), startColumn=3)
lfoStyle.create(["None", "Cutoff", "Volume"], width=10, variable="style")
lfoStyle.posVertical(padx=5, pady=15, gap=30)

#Radiobutton(sectionLFO.getSection(), variable=group, image=triR, value=1, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setStyle(1)]).grid(row=FIRST, column=THIRD, padx=5, pady=(0, 60))
#Radiobutton(sectionLFO.getSection(), variable=group, image=sawR, value=2, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setStyle(2)]).grid(row=FIRST, column=THIRD, padx=5, pady=10)
#Radiobutton(sectionLFO.getSection(), variable=group, image=sqareR, value=3, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setStyle(3)]).grid(row=FIRST, column=THIRD, padx=5, pady=(60, 0))
lfoSlider = SliderGroup(sectionLFO.getSection())
lfoSlider.create(["Amount", "Rate"], [synth.valueLfoAmount, synth.valueLfoRate])


tupleList = EffectPair(touchpad.parent)
tupleList.addOptions(oscillator.sliders[0], effects.sliders[1])
tupleList.addOptions(oscillator.sliders[0], lfoSlider.sliders[1])
tupleList.addOptions(lfoSlider.sliders[0], effects.sliders[1])
tupleList.addOptions(lfoSlider.sliders[0], lfoSlider.sliders[1])
touchpad.updateOptions(tupleList)

mainloop()
