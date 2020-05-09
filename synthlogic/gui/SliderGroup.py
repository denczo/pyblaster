from synthlogic.gui.Slider import Slider


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
