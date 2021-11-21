from tkinter import *
from random import randint

def moveShip(event):
    global ship, shipImage, shipImages

    # movement
    if event.keysym == "Left" or event.keysym == "a":
        canvas.move(ship, -15, 0)
    elif event.keysym == "Right" or event.keysym == "d":
        canvas.move(ship, 15, 0)
    elif event.keysym == "Up" or event.keysym == "w":
        canvas.move(ship, 0, -15)
    elif event.keysym == "Down" or event.keysym == "s":
        canvas.move(ship, 0, 15)

    # ship randomizer
    elif event.keysym == "f":
        s = canvas.coords(ship)
        l = len(shipImages)-1
        canvas.delete(ship)
        shipImage = shipImages[randint(0,l)]
        ship = canvas.create_image(s[0], s[1], image=shipImage)

def shipShoot(self):
    global shotAvailable

    # create box for getting the coords of the ship
    box = canvas.create_rectangle(canvas.bbox(ship), outline="")
    c = canvas.coords(box)
    halfx = (c[0] + c[2]) / 2

    if shotAvailable == 1:
        canvas.create_line(halfx,c[1]-30,halfx,c[1],width=4,fill="yellow",tag="shot")
        shotAvailable = 0
        shipShootUpdate("shot")

def shipShootUpdate(name):
    global shotAvailable

    canvas.move(name,0,-20)
    canvas.update()
        
    if shotAvailable == 0:
        shot = canvas.coords(name)
        # if bullet off screen, delete it
        if shot[1] < 0:
            canvas.delete(name)
            shotAvailable = 1

    # update animation when bullet still on screen
    if shotAvailable == 0:
        window.after(40, shipShootUpdate, name)

def setWindowDimensions(w,h):
    window = Tk()
    window.title("Space Invaders")
    ws = window.winfo_screenwidth() # computers screen size
    hs = window.winfo_screenheight()
    x = (ws/2) - (w/2) # calculates center
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y)) # sets window size
    return window

# set the screen size/resolution here
width = 1600
height = 900

x = width / 2
y = height / 2
window = setWindowDimensions(width, height)
canvas = Canvas(window, bg="black", width=width, height=height)
canvas.pack()

# create the player
shipImages = [PhotoImage(file="ships/ship1.png").subsample(5,5),
              PhotoImage(file="ships/ship2.png").subsample(6,6),
              PhotoImage(file="ships/ship3.png").subsample(6,6)]
shipImage = shipImages[0]
ship = canvas.create_image(x, x, image=shipImage)
shotAvailable = 1 # set shotAvailable to 1 at beginning of game

score = "Score: "
canvas.create_text(20, 20, anchor=NW, font="terminus 20 bold", text=score, fill="#3a852e")
health = "Health: "
canvas.create_text(20, 70, anchor=NW, font="terminus 20 bold", text=health, fill="#cc272a")

window.bind("<Key>", moveShip)
window.bind("<space>", shipShoot)

window.mainloop()