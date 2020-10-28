from tkinter import *
from PIL import Image, ImageTk

def Mousecoords(event):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    pointxy = (event.x, event.y) # get the mouse position from event
    if width > event.x > 0 and height > event.y > 0:
        print(pointxy)
        canvas.coords(cimg, pointxy) # move the image to mouse postion

def key(event):
    print("pressed", repr(event.char))

root = Tk()
img = ImageTk.PhotoImage(file='green.png')
canvas = Canvas(width=250, height=250)
cimg = canvas.create_image(200, 100, image=img)
canvas.pack()
#canvas.bind('<Motion>', Mousecoords) # track mouse movement
canvas.bind('<B1-Motion>', Mousecoords)
canvas.bind('<Button-1>', Mousecoords)
root.mainloop()