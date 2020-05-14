from tkinter import Radiobutton, N

from PIL import ImageTk


class Button:
    def __init__(self, parent, value, label, cmd=None,  width=0, height=0, variable=None):

        self.instance = Radiobutton(parent, value=value, variable=variable, indicatoron=0, width=width, height=height)
        if isinstance(label, str):
            self.instance.config(text=label)
        elif isinstance(label, ImageTk.PhotoImage):
            self.instance.config(image=label)
        else:
            raise TypeError('Wrong Type. Label must be of type String or PhotoImage!')

    def pos(self, row, column, padx=0, pady=0):
        self.instance.grid(row=row, column=column, padx=padx, pady=pady, sticky=N)



