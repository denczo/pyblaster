from tkinter import Radiobutton, N, StringVar

from PIL import ImageTk


class Button:
    def __init__(self, parent, value, label, stateCarrier, width=0, height=0, variable=None):

        self.instance = Radiobutton(parent, value=value, variable=variable, indicatoron=0, command=lambda: stateCarrier.saveVal(value), width=width, height=height)
        if isinstance(label, str):
            self.instance.config(text=label)
        elif isinstance(label, ImageTk.PhotoImage):
            self.instance.config(image=label)
        else:
            raise TypeError('Wrong Type. Label must be of type String or PhotoImage!')

    def pos(self, row, column, padx=0, pady=0):
        self.instance.grid(row=row, column=column, padx=padx, pady=pady, sticky=N)


class ButtonGroup:
    def __init__(self, parent, startRow=0, startColumn=0):
        self.parent = parent
        self.buttons = []
        self.currentRow = startRow
        self.currentColumn = startColumn
        self.selection = StringVar()
        self.selection.set(0)

    # creates group of buttons with labels or icons
    def create(self, labels, values, stateCarriers, width=0, height=0):
        for i in range(len(labels)):
            button = Button(self.parent, values[i], labels[i], stateCarriers[i], width=width, height=height, variable=self.selection)
            self.buttons.append(button)

    def posVertical(self, padx=0, pady=0, gap=0):

        if isinstance(pady, tuple):
            top = pady[0]
        else:
            top = pady

        for i in range(len(self.buttons)):
            self.buttons[i].pos(self.currentRow, self.currentColumn, padx=padx, pady=(top+i*gap, 0))
            #self.currentRow += 1
        self.currentColumn += 1

    def posHorizontal(self, padx=0, pady=0):
        for button in self.buttons:
            button.pos(self.currentRow, self.currentColumn, padx=padx, pady=pady)
            self.currentColumn += 1
        self.currentRow += 1

