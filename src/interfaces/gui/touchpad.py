from tkinter import *
from PIL import Image, ImageTk


class Touchpad:
    def __init__(self, parent, width, height, tp_state):
        self.parent = parent
        self.effectPair = None
        self.height = height
        self.width = width
        self.canvas = Canvas(parent, width=width, height=height, highlightthickness=0, relief='ridge', bg='#444')
        self.background = ImageTk.PhotoImage(Image.open('.//icons/touchpad/touchpad.gif').resize((width, height), Image.ANTIALIAS))
        self.canvas.create_image(0, 0, image=self.background, anchor=NW)
        self.cursor = ImageTk.PhotoImage(Image.open('.//icons/touchpad/cursor.png'))
        self.imageId = self.canvas.create_image(10, 10, image=self.cursor)
        self.canvas.itemconfig(self.imageId, image=self.cursor)
        self.canvas.bind('<B1-Motion>', self.mouseCoords)
        self.canvas.bind('<Button-1>', self.mouseCoords)
        self.canvas.bind('<ButtonRelease>', self.hideCursor)
        self.canvas.grid()
        self.x = 0
        self.y = 0
        self.tp_state = tp_state
        self.hideCursor(None)

        self.selectedOption = Label(parent)
        self.options = []

    def mouseCoords(self, event):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.tp_state.state = True

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
        self.tp_state.state = False
        self.canvas.itemconfigure(self.imageId, state=HIDDEN)

    def convert2Value(self, currentGiven, maxGiven, maxActual):
        ratio = float(maxActual/maxGiven)
        result = float(ratio*currentGiven)
        return result

    def setValues(self):
        xValue = self.convert2Value(self.x, self.width, 2)
        yValue = self.convert2Value(self.y, self.height, 2)
        if self.effectPair is not None:
            params = self.effectPair.valueCarriers()
            params[0].valueCarrier.value = xValue
            params[1].valueCarrier.value = yValue

        #self.synth.valueFrequency.setValue(xValue)
        #self.synth.valueCutoff.setValue(yValue)
