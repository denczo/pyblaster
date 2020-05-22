from tkinter import Scale, PhotoImage, Label, DISABLED, NORMAL


class Slider:
    def __init__(self, parent, label, valueCarrier, groupLabel=""):
        self.instance = Scale(parent, from_=2, to=0, resolution=0.02, length=100, showvalue=1, command=valueCarrier.saveVal)
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
        self.instance.grid(row=row, column=column, padx=(0, 20), pady=5)
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
