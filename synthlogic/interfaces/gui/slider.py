from tkinter import Scale, PhotoImage, Label, DISABLED, NORMAL, RIDGE, Button


class Slider:
    def __init__(self, parent, label, valueCarrier, groupLabel=""):
        self.instance = Scale(parent, from_=2, to=0, resolution=0.02, length=100, showvalue=0, command=valueCarrier.saveVal)
        self.valueCarrier = valueCarrier
        self.groupLabel = groupLabel
        self._label = None
        if isinstance(label, str):
            self._label = Label(parent, text=label)
        elif isinstance(label, PhotoImage):
            self._label = Label(parent, image=label)
        else:
            raise TypeError('Wrong Type. Label must be of type String or PhotoImage!')

    @property
    def label(self):
        return self._label.cget('text')

    # set pos for slider with label/icon
    def pos(self, row, column):
        self.instance.grid(row=row, column=column, padx=(21, 21), pady=5)
        self._label.grid(row=row+1, column=column)

    # activate or deactivate slider
    def changeState(self, state):
        if state == DISABLED:
            self.instance.config(state=DISABLED, fg="#808080")
            self._label.config(fg="#808080")
        elif state == NORMAL:
            self.instance.config(state=NORMAL, fg="#000000")
            self._label.config(fg="#000000")
        else:
            raise ValueError('Wrong State. State can be either DISABLED or NORMAL!')


class SliderGroup:
    def __init__(self, parent, label=""):
        self.label = label
        self.parent = parent
        self.sliders = []
        self.currentRow = 0
        self.currentColumn = 0

    # creates group of sliders with labels or icons, icons 40x40 px only
    def create(self, labels, valueCarriers):
        for i in range(len(labels)):
            slider = Slider(self.parent, labels[i], valueCarriers[i], self.label)
            self.sliders.append(slider)
            slider.pos(self.currentRow, self.currentColumn)
            self.currentColumn += 1
        self.currentRow += 1


class Selector:
    def __init__(self, parent, amount, data):
        self.amount = amount
        self.listIndex = 0
        self.labelIndex = Label(parent, text=self.listIndex, relief=RIDGE, width=2)
        self.leftButton = Button(parent, text="<<", command=lambda: [self.moveLeft(), self.updateLabel()])
        self.rightButton = Button(parent, text=">>", command=lambda: [self.moveRight(), self.updateLabel()])
        self.pos(1, 0)
        self.data = data

    def moveLeft(self):
        self.listIndex -= 1
        self.listIndex %= self.amount

    def moveRight(self):
        self.listIndex += 1
        self.listIndex %= self.amount

    def updateLabel(self):
        self.labelIndex.configure(text=self.listIndex)
        self.data.harm_amount = self.listIndex

    def pos(self, row, column):
        self.labelIndex.grid(row=row, column=column)
        self.leftButton.grid(row=row, column=column, padx=(80, 152), pady=5)
        self.rightButton.grid(row=row, column=column, padx=(152, 80), pady=5)


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