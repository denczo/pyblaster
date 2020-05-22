from tkinter import *


class EffectPair:
    def __init__(self, parent):
        self.listIndex = 0
        self.combinations = []
        self.descriptions = []
        self.labelIndex = Label(parent, text=self.listIndex, relief=RIDGE, width=2)
        self.label = Label(parent, anchor='w', relief=RIDGE, width=20)
        self.leftButton = Button(parent, text="<<", command=lambda: [self.moveLeft(), self.updateLabel()])
        self.rightButton = Button(parent, text=">>", command=lambda: [self.moveRight(), self.updateLabel()])
        self.pos(1, 0)

    def moveLeft(self):
        self.enableSlider(self.listIndex)
        self.listIndex -= 1
        self.listIndex %= len(self.descriptions)
        self.disableSlider(self.listIndex)

    def moveRight(self):
        self.enableSlider(self.listIndex)
        self.listIndex += 1
        self.listIndex %= len(self.descriptions)
        self.disableSlider(self.listIndex)

    # TODO improve code
    def enableSlider(self, index):
        self.combinations[index][0].changeState(NORMAL)
        self.combinations[index][1].changeState(NORMAL)

    def disableSlider(self, index):
        self.combinations[index][0].changeState(DISABLED)
        self.combinations[index][1].changeState(DISABLED)

    def valueCarriers(self):
        return self.combinations[self.listIndex]

    def updateLabel(self):
        self.label.configure(text=self.descriptions[self.listIndex])
        self.labelIndex.configure(text=self.listIndex)

    def pos(self, row, column):
        self.label.grid(row=row, column=column, padx=(20, 0))
        self.labelIndex.grid(row=row, column=column, padx=(0, 150))
        self.leftButton.grid(row=row, column=column, padx=(0, 200), pady=5)
        self.rightButton.grid(row=row, column=column, padx=(200, 0), pady=5)

    # TODO improve code
    def addOptions(self, sliderX, sliderY):
        description = sliderX.groupLabel + " " + sliderX.label + " : " + sliderY.groupLabel + " " + sliderY.label
        self.descriptions.append(description)
        self.combinations.append([sliderX, sliderY])
        self.updateLabel()
