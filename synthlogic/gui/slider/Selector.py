from tkinter import Label, Button, RIDGE


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
