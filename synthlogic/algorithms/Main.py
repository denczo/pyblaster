from synthlogic.algorithms.Synth import Synth
from synthlogic.gui.UserInterface import UserInterface


def main():
    synth = Synth()
    gui = UserInterface("EARDRUM BLASTER", 558, 650, synth)
    gui.render()


if __name__ == "__main__":
    main()
