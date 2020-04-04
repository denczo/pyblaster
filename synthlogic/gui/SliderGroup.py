from tkinter import *


class SliderGroup(Tk):
    def __init__(self, parent):
        self.parent = parent
        self.sliders = []
        self.currentRow = 0
        self.currentColumn = 0

    def createSlider(self, valueCarriers):

        for i in range(len(valueCarriers)):
            slider = Scale(self.parent, from_=100, to=0, length=100, command=valueCarriers[i].setValue)
            slider.grid(row=self.currentRow, column=self.currentColumn, padx=(0, 20), pady=5)
            self.currentColumn += 1
        self.currentColumn = 0
        self.currentRow += 1

    def createLabels(self, labels):

        for i in range(len(labels)):
            Label(self.parent, text=labels[i]).grid(row=self.currentRow, column=self.currentColumn)
            self.currentColumn += 1
        self.currentColumn = 0
        self.currentRow += 1

    # icons of size 40x40 px
    def createIcons(self, icons):

        for i in range(len(icons)):
            icon = icons[i]
            Label(self.parent, image=icon).grid(row=self.currentRow, column=self.currentColumn)
            self.currentColumn += 1
        self.currentColumn = 0
        self.currentRow += 1



# #DMCA Report - https://ya-webdesign.com/image/sine-wave-png/2072118.html
# master = Tk()
# master.title("EARDRUM BLASTER")
# master.resizable(width=False, height=False)
# winWidth = 468
# winHeight = 565
# windowSize = str(winHeight)+'x'+str(winHeight)
# master.geometry(windowSize)
# screenWidth = master.winfo_screenwidth()
# screenHeight = master.winfo_screenheight()
# startX = int((screenWidth/2) - (winWidth/2))
# startY = int((screenHeight/2) - (winHeight/2))
# master.geometry('{}x{}+{}+{}'.format(winWidth, winHeight, startX, startY))
#
#
# LABELFRAME_BG = '#444'
# LABELFRAME_FG = 'white'
#
# sectionOsc = Section(master,"OSCILLATOR", LABELFRAME_FG, LABELFRAME_BG)
# sectionOsc.setPosition(0, 0, 3, 5, 5)
# oscillator = SliderGroup(sectionOsc.getSection())
#
#
# sineIcon = PhotoImage(file="../icons_new/sine.png")
# triangleIcon = PhotoImage(file="../icons_new/triangle.png")
# sawtoothIcon = PhotoImage(file="../icons_new/sawtooth.png")
# squareIcon = PhotoImage(file="../icons_new/square.png")
#
# oscillator.createIcons([sineIcon,triangleIcon,sawtoothIcon,squareIcon])
# oscillator.createSlider()
#
# sectionFilter = Section(master,"FILTER", LABELFRAME_FG, LABELFRAME_BG)
# sectionFilter.setPosition(5, 0, 3, 5, 5)
# effects = SliderGroup(sectionFilter.getSection())
# effects.createSlider()
# effects.createLabels(["Cutoff", "Reverb", "Delay", "Flanger"])
#
# #oscillator.createLabels(["Sine","Square","Sawtooth","Triangle"])
#
# mainloop()


