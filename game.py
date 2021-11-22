from tkinter import *
from random import randint

def playerControls(event):
    global player, playerModels

    # movement / old
    # if event.keysym in leftBinds:
    #     canvas.move(player, -15, 0)
    # elif event.keysym in rightBinds:
    #     canvas.move(player, 15, 0)
    # elif event.keysym in upBinds:
    #     canvas.move(player, 0, -15)
    # elif event.keysym in downBinds:
    #     canvas.move(player, 0, 15)

    # ship randomizer
    if event.keysym == "r":
        s = canvas.coords(player)
        l = len(playerModels)-1
        canvas.delete(player)
        playerImageRandom = playerModels[randint(0,l)]
        player = canvas.create_image(s[0], s[1], image=playerImageRandom)

def generateMoveStatus():
    # create a dictionary of binds
    moveStatus[leftBinds] = False
    moveStatus[rightBinds] = False
    moveStatus[upBinds] = False
    moveStatus[downBinds] = False

def setMoveBinds():
    for char in leftBinds:
        window.bind("<KeyPress-%s>" % char, moveKeyPressed)
        window.bind("<KeyRelease-%s>" % char, moveKeyReleased)
    for char in rightBinds:
        window.bind("<KeyPress-%s>" % char, moveKeyPressed)
        window.bind("<KeyRelease-%s>" % char, moveKeyReleased)
    for char in upBinds:
        window.bind("<KeyPress-%s>" % char, moveKeyPressed)
        window.bind("<KeyRelease-%s>" % char, moveKeyReleased)
    for char in downBinds:
        window.bind("<KeyPress-%s>" % char, moveKeyPressed)
        window.bind("<KeyRelease-%s>" % char, moveKeyReleased)

def moveKeyPressed(event):
    # set bind true if pressed
    if event.keysym in leftBinds:
        moveStatus[leftBinds] = True
    if event.keysym in rightBinds:
        moveStatus[rightBinds] = True
    if event.keysym in upBinds:
        moveStatus[upBinds] = True
    if event.keysym in downBinds:
        moveStatus[downBinds] = True

    # if bind is set to true then move player
    if moveStatus[leftBinds] == True: canvas.move(player, -15, 0)
    if moveStatus[rightBinds] == True: canvas.move(player, 15, 0)
    if moveStatus[upBinds] == True: canvas.move(player, 0, -15)
    if moveStatus[downBinds] == True: canvas.move(player, 0, 15)

def moveKeyReleased(event):
    # set bind false if released
    if event.keysym in leftBinds:
        moveStatus[leftBinds] = False
    if event.keysym in rightBinds:
        moveStatus[rightBinds] = False
    if event.keysym in upBinds:
        moveStatus[upBinds] = False
    if event.keysym in downBinds:
        moveStatus[downBinds] = False

def playerShoot(self):
    global shotAvailable

    # create box for getting the coords of the ship
    box = canvas.create_rectangle(canvas.bbox(player), outline="")
    c = canvas.coords(box)
    halfx = (c[0] + c[2]) / 2

    if shotAvailable == 1:
        canvas.create_line(halfx,c[1]-30,halfx,c[1],width=4,fill="yellow",tag="shot")
        shotAvailable = 0
        playerShootUpdate("shot")

def playerShootUpdate(name):
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
    # using another if to prevent speeding up bullet
    if shotAvailable == 0:
        window.after(40, playerShootUpdate, name)

def bossKey(event):
    global bossKeyToggle, bossKeyLabel, window
    bossKeyToggle ^= 1 # alternate toggle between 1 and 0

    if bossKeyToggle == 1:
        bossKeyLabel.image = bossKeyImage
        bossKeyLabel.place(relx=0.5, rely=0.5, anchor="center")
        window.title("Microsoft Excel - Employees.xlsx")

    elif bossKeyToggle == 0:
        bossKeyLabel.place_forget()
        window.title("Space Invaders")

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
playerModels = [PhotoImage(file="ships/ship1.png").subsample(5),
                PhotoImage(file="ships/ship2.png").subsample(7),
                PhotoImage(file="ships/ship3.png").subsample(7)]
playerImage = playerModels[0]
player = canvas.create_image(x, height-100, image=playerImage)
shotAvailable = 1 # set shotAvailable to 1 at beginning of game

# setup boss key
bossKeyToggle = 0
bossKeyImage = PhotoImage(file="misc/bosskey.png")
bossKeyLabel = Label(canvas, image=bossKeyImage, height=height, width=width)

# set score and health
scoreText = "Score: "
canvas.create_text(20, 20, anchor=NW, font="terminus 20 bold", text=scoreText, fill="#3a852e")
healthText = "Health: "
canvas.create_text(20, 70, anchor=NW, font="terminus 20 bold", text=healthText, fill="#cc272a")

# setup keybindings
moveStatus = {}
leftBinds = ("Left", "a")
rightBinds = ("Right", "d")
upBinds = ("Up", "w")
downBinds = ("Down", "s")
generateMoveStatus()
setMoveBinds()

window.bind("<Key>", playerControls)
window.bind("<Control-b>", bossKey)
window.bind("<space>", playerShoot)

window.mainloop()