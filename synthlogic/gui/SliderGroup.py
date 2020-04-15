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
