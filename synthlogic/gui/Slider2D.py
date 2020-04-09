from tkinter import *
from PIL import Image, ImageTk


class Slider2D(Tk):
    def __init__(self, parent, width, height, synth):
        self.parent = parent
        self.synth = synth
        self.height = height
        self.width = width
        self.canvas = Canvas(parent, width=width, height=height, highlightthickness=0, relief='ridge')
        self.background = ImageTk.PhotoImage(Image.open('touchpad_new.gif').resize((width, height), Image.ANTIALIAS))
        self.canvas.create_image(0, 0, image=self.background, anchor=NW)
        self.cursor = ImageTk.PhotoImage(Image.open('cursor.png'))
        self.imageId = self.canvas.create_image(10, 10, image=self.cursor)
        self.canvas.itemconfig(self.imageId, image=self.cursor)
        self.canvas.bind('<B1-Motion>', self.mouseCoords)
        self.canvas.bind('<Button-1>', self.mouseCoords)
        self.canvas.bind('<ButtonRelease>', self.hideCursor)
        self.canvas.grid()
        self.x = 0
        self.y = 0

    def mouseCoords(self, event):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        pointxy = (event.x, event.y)
        if width > event.x > 0 and height > event.y > 0:
            self.x = event.x
            self.y = event.y
            #print(pointxy)
            self.canvas.itemconfigure(self.imageId, state=NORMAL)
            self.canvas.coords(self.imageId, pointxy)
            self.setValues()

    def hideCursor(self, event):
        self.canvas.itemconfigure(self.imageId, state=HIDDEN)

    def convert2Value(self, currentGiven, maxGiven, maxActual):
        ratio = float(maxActual/maxGiven)
        result = float(ratio*currentGiven)
        return result

    def setValues(self):
        xValue = self.convert2Value(self.x, self.width, 1000)
        #print(xValue)
        self.synth.valueFrequency.setValue(xValue)
        #print(self.synth.valueFrequency.getValue())