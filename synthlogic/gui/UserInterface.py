import threading
from tkinter import Tk, messagebox, PhotoImage, E, W, Radiobutton, StringVar, Label

from PIL import ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from synthlogic.gui.Grid import Grid
from synthlogic.gui.Section import Section
from synthlogic.gui.Touchpad import Touchpad
from synthlogic.gui.SliderGroup import SliderGroup


class UserInterface:
    def __init__(self, name, width, height, synth):
        self.master = Tk()
        screenWidth = int(self.master.winfo_width())
        screenHeight = int(self.master.winfo_height())
        x = int(screenWidth / 2 - int(width) / 2)
        y = int(screenHeight / 2 - int(height) / 2)
        #self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.master.resizable(width=False, height=False)
        self.master.title = name
        self.master.protocol("WM_DELETE_WINDOW", self.onClose)
        self.background = ImageTk.PhotoImage(file='../icons/background/scratch.jpg')
        self.touchpad_bg = PhotoImage(file='../icons/touchpad/touchpad.gif')
        self.background_label = Label(image=self.background)
        self.background_label.image = self.background
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.fig = None
        self.axis = None
        self.canvas = None

        self.synth = synth
        # sliders
        self.oscillator = []
        self.envelope = []
        self.effects = []

    def onClose(self):
        close = messagebox.askokcancel("Close", "Would you like to close the EARDRUM BLASTER?")
        if close:
            self.synth.running = False
            self.master.destroy()

    def loadImage(self, paths):
        loadedImages = []
        for i in range(len(paths)):
            image = PhotoImage(file=paths[i])
            loadedImages.append(image)
        return loadedImages

    def updatePlot(self):
        self.axis.cla()
        self.axis.set_xticks([], [])
        self.axis.set_yticks([], [])
        self.axis.spines['top'].set_visible(False)
        self.axis.spines['right'].set_visible(False)
        self.axis.spines['bottom'].set_visible(False)
        self.axis.spines['left'].set_visible(False)

        self.axis.plot(self.synth.x[:1024], self.synth.y[:1024])
        self.fig.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9)

        self.canvas.draw()
        # every 10ms; raise, to improve performance
        self.master.after(1000, self.updatePlot)

    def oscillatorSection(self):
        sineIcon = PhotoImage(file="../icons/waveforms/Sine.png")
        triangleIcon = PhotoImage(file="../icons/waveforms/Triangle.png")
        sawtoothIcon = PhotoImage(file="../icons/waveforms/Sawtooth.png")
        squareIcon = PhotoImage(file="../icons/waveforms/Square.png")

        sectionOsc = Section(self.master, "OSCILLATOR", Grid.LABELFRAME_FG, Grid.LABELFRAME_BG)
        sectionOsc.setPosition(Grid.FIRST, Grid.FIRST, 2, 1, Grid.PAD_X, Grid.PAD_Y)
        self.oscillator = SliderGroup(sectionOsc.getSection())
        self.oscillator.createIcons([sineIcon, triangleIcon, sawtoothIcon, squareIcon])
        self.oscillator.createSlider( [self.synth.valueSine, self.synth.valueTriangle, self.synth.valueSawtooth, self.synth.valueSquare])

    def styleSection(self):

        monoIcon = PhotoImage(file="../icons/style/mono.png")
        duoIcon = PhotoImage(file="../icons/style/duo.png")
        trioIcon = PhotoImage(file="../icons/style/trio.png")
        quattroIcon = PhotoImage(file="../icons/style/quattro.png")

        # default selection
        group = StringVar()
        group.set(1)
        sectionStyle = Section(self.master, "STYLE", Grid.LABELFRAME_FG, Grid.LABELFRAME_BG)
        sectionStyle.setPosition(Grid.THIRD, Grid.FIRST, 1, 1, Grid.PAD_X, (0, Grid.PAD_Y))
        Radiobutton(sectionStyle.getSection(), variable=group, image=monoIcon, value=1, indicatoron=0, width=Grid.WIDTH_IMG, height=Grid.HEIGHT_RB, command=lambda: [self.synth.setStyle(1)]).grid(row=Grid.FIRST, column=Grid.FIRST, padx=(6, 0), pady=(Grid.PAD_Y_W, 0))
        Radiobutton(sectionStyle.getSection(), variable=group, image=duoIcon, value=2, indicatoron=0, width=Grid.WIDTH_IMG, height=Grid.HEIGHT_RB, command=lambda: [self.synth.setStyle(2)]).grid(row=Grid.FIRST, column=Grid.SECOND, padx=(5, 0), pady=(Grid.PAD_Y_W, 0))
        Radiobutton(sectionStyle.getSection(), variable=group, image=trioIcon, value=3, indicatoron=0, width=Grid.WIDTH_IMG, height=Grid.HEIGHT_RB, command=lambda: [self.synth.setStyle(3)]).grid(row=Grid.FIRST, column=Grid.THIRD, padx=(5, 0), pady=Grid.PAD_Y_W)
        Radiobutton(sectionStyle.getSection(), variable=group, image=quattroIcon, value=4, indicatoron=0, width=Grid.WIDTH_IMG, height=Grid.HEIGHT_RB, command=lambda: [self.synth.setStyle(4)]).grid(row=Grid.FIRST, column=Grid.FOURTH, padx=(5, 7), pady=Grid.PAD_Y_W)

    def chunkSection(self):
        sectionChunk = Section(self.master, "CHUNK", Grid.LABELFRAME_FG, Grid.LABELFRAME_BG)
        sectionChunk.setPosition(Grid.FOURTH, Grid.FIRST, 1, 1, Grid.PAD_X, (0, Grid.PAD_Y))
        self.fig = Figure(figsize=(2.6, 1), facecolor='#F0F0F0')
        self.axis = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=sectionChunk.getSection())
        self.canvas._tkcanvas.grid(row=Grid.FIRST, column=Grid.FIRST, sticky=E + W)
        t = threading.Thread(target=self.updatePlot())
        t.start()

    def touchpadSection(self, synth):
        sectionTouchpad = Section(self.master, "TOUCH ME", Grid.LABELFRAME_FG, Grid.LABELFRAME_BG)
        sectionTouchpad.setPosition(Grid.FIFTH, Grid.FIRST, 2, 1, Grid.PAD_X, (0, Grid.PAD_Y))
        touchpad = Touchpad(sectionTouchpad.getSection(), 260, 195, synth)

    def envelopeSection(self):
        sectionEnv = Section(self.master, "ENVELOPE", Grid.LABELFRAME_FG, Grid.LABELFRAME_BG)
        sectionEnv.setPosition(Grid.FIRST, Grid.SECOND, 1, 1, (0, Grid.PAD_X), Grid.PAD_Y)
        self.envelope = SliderGroup(sectionEnv.getSection())
        self.envelope.createSlider([self.synth.valueAttack, self.synth.valueDecay, self.synth.valueSustain, self.synth.valueRelease])
        self.envelope.createLabels(["Attack", "Decay", "Sustain", "Release"])

    def filterSection(self):
        sectionFilter = Section(self.master, "FILTER", Grid.LABELFRAME_FG, Grid.LABELFRAME_BG)
        sectionFilter.setPosition(Grid.THIRD, Grid.SECOND, 2, 2, (0, Grid.PAD_X), 0)
        self.effects = SliderGroup(sectionFilter.getSection())
        self.effects.createSlider([self.synth.valueReverb, self.synth.valueCutoff])
        self.effects.createLabels(["Reverb", "Cutoff"])

    def render(self):

        self.oscillatorSection()
        self.styleSection()
        self.chunkSection()
        self.touchpadSection(self.synth)
        self.envelopeSection()
        self.filterSection()
        self.master.mainloop()
