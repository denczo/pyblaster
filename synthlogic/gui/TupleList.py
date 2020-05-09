from tkinter import *

# TODO FIX NAME
class TupleList:
    def __init__(self, parent):
        self.listIndex = 0
        self.combinations = []
        self.descriptions = []
        self.labelIndex = Label(parent, text=self.listIndex, relief=RIDGE, width=2)
        self.label = Label(parent, anchor='w', relief=RIDGE, width=20)
        self.leftButton = Button(parent, text="<<", command=lambda: [self.moveLeft(), self.updatePos()])
        self.rightButton = Button(parent, text=">>", command=lambda: [self.moveRight(), self.updatePos()])
        self.tuplePos(0,0)

    def moveLeft(self):
        self.enableSlider(self.listIndex)
        self.listIndex -= 1
        #print(self.listIndex)
        self.listIndex %= len(self.descriptions)
        self.disableSlider(self.listIndex)

    def moveRight(self):
        self.enableSlider(self.listIndex)
        self.listIndex += 1
        #print(self.listIndex)
        self.listIndex %= len(self.descriptions)
        self.disableSlider(self.listIndex)

    def enableSlider(self, index):
        self.combinations[index][0].changeState(NORMAL)
        self.combinations[index][1].changeState(NORMAL)

    def disableSlider(self, index):
        self.combinations[index][0].changeState(DISABLED)
        self.combinations[index][1].changeState(DISABLED)

    def valueCarriers(self):
        return self.combinations[self.listIndex]

    def updatePos(self):
        self.label.configure(text=self.descriptions[self.listIndex])
        self.labelIndex.configure(text=self.listIndex)

    def tuplePos(self, row, column):
        self.label.grid(row=0, column=0, padx=(20, 0))
        self.labelIndex.grid(row=0, column=0, padx=(0, 150))
        self.leftButton.grid(row=0, column=0, padx=(0, 200), pady=5)
        self.rightButton.grid(row=0, column=0, padx=(200, 0), pady=5)

    def addOptions(self, sliderX, sliderY):
        description = sliderX.groupLabel + " " + sliderX.label + " : " + sliderY.groupLabel + " " + sliderY.label
        self.descriptions.append(description)
        self.combinations.append([sliderX, sliderY])
