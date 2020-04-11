from tkinter import *


class Section(Tk):
    # bg = background, fg = foreground
    def __init__(self, parent, headline, fg, bg):
        self.border = LabelFrame(parent, text=headline, fg=fg, bg=bg, relief=FLAT)
        self.innerBox = None
        self.section = None
        self.row = 0
        self.column = 0

    def setPosition(self, row, column, rowspan, columnspan, padx, pady):
        self.border.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=padx, pady=pady, sticky=N+W)
        self.innerBox = Frame(self.border)
        self.innerBox.grid()
        self.section = self.innerBox

    def getSection(self):
        return self.section
