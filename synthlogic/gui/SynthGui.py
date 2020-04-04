from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from synthlogic.algorithms.Synth import Synth
import threading

from synthlogic.gui.Section import Section
from synthlogic.gui.SliderGroup import SliderGroup

master = Tk()
master.title("EARDRUM BLASTER")
master.resizable(width=False, height=False)
winWidth = 365
winHeight = 600
windowSize = str(winHeight)+'x'+str(winHeight)
master.geometry(windowSize)
screenWidth = master.winfo_screenwidth()
screenHeight = master.winfo_screenheight()
startX = int((screenWidth/2) - (winWidth/2))
startY = int((screenHeight/2) - (winHeight/2))
master.geometry('{}x{}+{}+{}'.format(winWidth, winHeight, startX, startY))

synth = Synth()

def updatePlot():
    global axis, canvas

    axis.cla()
    #axis.grid()
    axis.set_yticklabels([])
    axis.set_xticklabels([])
    axis.plot(synth.x, synth.y, color='black')
    canvas.draw()
    # every 10ms; raise, to improve performance
    master.after(10, updatePlot)


def updateBtnText():
    playBtn.configure(text=synth.status)

WIDTH_IMG = 50
WIDTH_RB = WIDTH_IMG
HEIGHT_RB = WIDTH_RB

FIRST = 0
SECOND = FIRST + 1
THIRD = SECOND + 1
FOURTH = THIRD + 1

PAD_X = 10
PAD_Y = 10
PAD_X_W = 5
PAD_Y_W = 5

background_image = PhotoImage(file='../background.gif')
#Photo by mohammad alizade on Unsplash
#Photo by Paweł Czerwiński on Unsplash
background_label = Label(image=background_image)
background_label.image = background_image
background_label.place(x=0, y=0, relwidth=1, relheight=1)
#master.configure(background='#690008')

# matplotlib
fig = Figure(figsize=(2.6, 2), facecolor='#F0F0F0')
axis = fig.add_subplot(111)

#LABELFRAME_BG = '#053E7E'
#LABELFRAME_BG = '#A60000'
LABELFRAME_BG = '#444'
LABELFRAME_FG = 'white'

# border with label
styleGroup = LabelFrame(master, text="STYLE", fg=LABELFRAME_FG, bg=LABELFRAME_BG, relief=FLAT)
freqGroup = LabelFrame(master, text="FREQUENCY", fg=LABELFRAME_FG, bg=LABELFRAME_BG, relief=FLAT)

# group of widgets
styleGroup.grid(row=SECOND, column=FIRST, rowspan=1, padx=PAD_X, pady=(0, PAD_Y), sticky=N+E+W)
freqGroup.grid(row=THIRD, column=FIRST, rowspan=1, padx=PAD_X, pady=(0, PAD_Y), sticky=N+E+W)

# gray inner box
frameStyle = Frame(styleGroup)
frameFreq = Frame(freqGroup)

frameStyle.grid(sticky=E+W)
frameFreq.grid(sticky=E+W)

canvas = FigureCanvasTkAgg(fig, master=frameFreq)
t = threading.Thread(target=updatePlot())
t.start()

# default selection
group1 = StringVar()
group2 = StringVar()
group1.set(1)
group2.set(1)

sineIcon = PhotoImage(file="../icons_new/Sine.png")
triangleIcon = PhotoImage(file="../icons_new/Triangle.png")
sawtoothIcon = PhotoImage(file="../icons_new/Sawtooth.png")
squareIcon = PhotoImage(file="../icons_new/Square.png")

# oscillator section
sectionOsc = Section(master, "OSCILLATOR", LABELFRAME_FG, LABELFRAME_BG)
sectionOsc.setPosition(FIRST, FIRST, 1, PAD_X, PAD_Y)
oscillator = SliderGroup(sectionOsc.getSection())
oscillator.createIcons([sineIcon, triangleIcon, sawtoothIcon, squareIcon])
oscillator.createSlider([synth.valueSine, synth.valueTriangle, synth.valueSawtooth, synth.valueSquare])


# style options
monoIcon = PhotoImage(file="../icons/mono.png")
duoIcon = PhotoImage(file="../icons/duo.png")
trioIcon = PhotoImage(file="../icons/trio.png")
quattroIcon = PhotoImage(file="../icons/quattro.png")

Radiobutton(frameStyle, variable=group2, image=monoIcon, value=1, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setStyle(1)]).grid(row=FIRST,column=FIRST, padx=(6,0), pady=(PAD_Y_W, 0))
Radiobutton(frameStyle, variable=group2, image=duoIcon, value=2, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setStyle(2)]).grid(row=FIRST,column=SECOND, padx=(5,0), pady=(PAD_Y_W, 0))
Radiobutton(frameStyle, variable=group2, image=trioIcon, value=3, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setStyle(3)]).grid(row=FIRST,column=THIRD, padx=(5,0), pady=PAD_Y_W)
Radiobutton(frameStyle, variable=group2, image=quattroIcon, value=4, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setStyle(4)]).grid(row=FIRST,column=FOURTH, padx=(5,7), pady=PAD_Y_W)

# frequency
canvas._tkcanvas.grid(row=FIRST, column=FIRST, columnspan=3)
w = Scale(frameFreq, from_=0, to=1000, length=200, orient=HORIZONTAL, resolution=1, command=lambda x: [synth.setFrequency(x)]).grid(row=SECOND, column=FIRST, columnspan=3, sticky=E+W, padx=PAD_X_W, pady=0)
playBtn = Button(frameFreq, text=synth.status, command=lambda: [synth.toggle(), updateBtnText()])
playBtn.grid(row=THIRD, column=FIRST, columnspan=3, sticky=E+W, padx=PAD_X_W, pady=PAD_Y_W)

# envelope section
sectionEnv = Section(master, "ENVELOPE", LABELFRAME_FG, LABELFRAME_BG)
sectionEnv.setPosition(FIRST, SECOND, 2, (0, PAD_X), PAD_Y)
effects = SliderGroup(sectionEnv.getSection())
effects.createSlider([synth.valueAttack])
effects.createLabels(["Attack"])

# filter section
sectionFilter = Section(master, "FILTER", LABELFRAME_FG, LABELFRAME_BG)
sectionFilter.setPosition(THIRD, SECOND, 1, (0, PAD_X), (0, PAD_Y))
effects = SliderGroup(sectionFilter.getSection())
effects.createSlider([synth.valueReverb])
effects.createLabels(["Reverb"])

mainloop()
