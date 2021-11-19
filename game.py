from tkinter import *

def setWindowDimensions(w,h):
    window = Tk()
    window.title("Space Invaders")
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    return window

width = 1920
height = 1080

window = setWindowDimensions(width, height)
canvas = Canvas(window, bg="black", width=width, height=height)

window.mainloop()