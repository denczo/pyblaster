from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from synthlogic.Synth import Synth
import threading

master = Tk()
master.title("EARDRUM BLASTER")


# all rows and columns scaleable
for i in range(3):
    Grid.rowconfigure(master, i, weight=1)
    Grid.columnconfigure(master, i, weight=1)

# synth
synth = Synth()

def updatePlot():
    global axis, canvas

    axis.cla()
    #axis.grid()
    axis.set_yticklabels([])
    axis.set_xticklabels([])
    axis.plot(synth.x, synth.y)
    canvas.draw()
    master.after(10, updatePlot)



# matplotlib
fig = Figure(figsize=(3, 3),facecolor='#f0f0f0')
axis = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=master)

t = threading.Thread(target=updatePlot())
t.start()
#updatePlot()

group1 = StringVar()
group2 = StringVar()
group1.set(1)
group2.set(1)

# waveform options
Label(master, text="WAVEFORM: ").grid(row=0,column=0, sticky=W, padx=5, pady=5)
Radiobutton(master, variable=group1, text="Sine", value=1, indicatoron=0, width=20, command=lambda: [synth.setWaveform(0)]).grid(row=0,column=1, padx=5, pady=5)
Radiobutton(master, variable=group1, text="Triangle", value=2, indicatoron=0, width=20, command=lambda: [synth.setWaveform(1)]).grid(row=0,column=2, padx=5, pady=5)
Radiobutton(master, variable=group1, text="Sawtooth", value=3, indicatoron=0, width=20, command=lambda: [synth.setWaveform(2)]).grid(row=1,column=1, padx=2)
Radiobutton(master, variable=group1, text="Square", value=4, indicatoron=0, width=20, command=lambda: [synth.setWaveform(3)]).grid(row=1,column=2, padx=2)

# style options
Label(master, text="STYLE: ").grid(row=2,column=0, sticky=W, padx=5, pady=5)
Radiobutton(master, variable=group2, text="Mono", value=1, indicatoron=0, width=20, command=lambda: [synth.setStyle(1)]).grid(row=2,column=1, padx=5, pady=5)
Radiobutton(master, variable=group2, text="Duo", value=2, indicatoron=0, width=20, command=lambda: [synth.setStyle(2)]).grid(row=2,column=2, padx=5, pady=5)
Radiobutton(master, variable=group2, text="Trio", value=3, indicatoron=0, width=20, command=lambda: [synth.setStyle(3)]).grid(row=3,column=1, padx=5)
Radiobutton(master, variable=group2, text="Quad", value=4, indicatoron=0, width=20, command=lambda: [synth.setStyle(4)]).grid(row=3,column=2, padx=5)
#w = OptionMenu(master, variable, "one", "two", "three")

# slider
w_label = Label(master, text="FREQUENCY: ").grid(row=4,column=0, sticky=W, padx=5, pady=5)
#w = Scale(master, from_=0, to=1000, length=200, orient=HORIZONTAL, resolution=15, command=lambda x: [synth.setFrequency(x), updatePlot()]).grid(row=2,column=1, columnspan=2, sticky=N+S+E+W, padx=5)
w = Scale(master, from_=0, to=1000, length=200, orient=HORIZONTAL, resolution=1, command=lambda x: [synth.setFrequency(x)]).grid(row=4,column=1, columnspan=2, sticky=N+S+E+W, padx=5, pady=5)

# button
Button(master, text='Play', command=lambda: [synth.toggle()]).grid(row=5, column=1, columnspan=2, sticky=N+S+E+W, padx=5)
canvas._tkcanvas.grid(row=6,sticky=W+E+N+S,columnspan=3, padx=5, pady=5)

# envelope
e_label = Label(master, text="ENVELOPE GEN: ").grid(row=7,column=0, sticky=W, padx=5)
attack = Scale(master, label="Attack",from_=100, to=0, length=100, command=synth.envGen.setAttack).grid(row=7,column=1, sticky=N+S+E+W, pady=5)
#decay = Scale(master, label="Decay",from_=100, to=0, length=100).grid(row=6,column=2, sticky=N+S+E+W, pady=5)

mainloop()