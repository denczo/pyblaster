from tkinter import *
from PIL import Image, ImageTk


class Touchpad:
    def __init__(self, parent, width, height, synth):
        self.parent = parent
        self.synth = synth
        self.effectPair = None
        self.height = height
        self.width = width
        self.canvas = Canvas(parent, width=width, height=height, highlightthickness=0, relief='ridge')
        self.background = ImageTk.PhotoImage(Image.open('../icons/touchpad/touchpad_new.gif').resize((width, height), Image.ANTIALIAS))
        self.canvas.create_image(0, 0, image=self.background, anchor=NW)
        self.cursor = ImageTk.PhotoImage(Image.open('../icons/touchpad/cursor.png'))
        self.imageId = self.canvas.create_image(10, 10, image=self.cursor)
        self.canvas.itemconfig(self.imageId, image=self.cursor)
        self.canvas.bind('<B1-Motion>', self.mouseCoords)
        self.canvas.bind('<Button-1>', self.mouseCoords)
        self.canvas.bind('<ButtonRelease>', self.hideCursor)
        self.canvas.grid()
        self.x = 0
        self.y = 0
        self.hideCursor(None)
        self.pressed = False

        self.selectedOption = Label(parent)
        self.options = []


    def mouseCoords(self, event):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.synth.valueStatus.setValue(True)

        self.x = 0
        self.y = 0

        if width >= event.x >= 0:
            self.x = event.x

        if height >= event.y >= 0:
            self.y = event.y

        if event.y > height > 0:
            self.y = self.height

        if event.x > width > 0:
            self.x = self.width

        pointxy = (self.x, self.y)
        self.canvas.itemconfigure(self.imageId, state=NORMAL)
        self.canvas.coords(self.imageId, pointxy)
        self.setValues()

    def updateOptions(self, effectPair):
        self.effectPair = effectPair

    def hideCursor(self, event):
        self.synth.valueStatus.setValue(False)
        self.canvas.itemconfigure(self.imageId, state=HIDDEN)

    def convert2Value(self, currentGiven, maxGiven, maxActual):
        ratio = float(maxActual/maxGiven)
        result = float(ratio*currentGiven)
        return result

    def setValues(self):
        xValue = self.convert2Value(self.x, self.width, 2)
        yValue = self.convert2Value(self.y, self.height, 2)
        if self.effectPair is not None:
            # TODO FIX
            params = self.effectPair.combinations[0]
            params[0].valueCarrier.setValue(xValue)
            params[1].valueCarrier.setValue(yValue)
        #self.synth.valueFrequency.setValue(xValue)
        #self.synth.valueCutoff.setValue(yValue)
