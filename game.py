from tkinter import *
from random import randint

def playerControls(event):
    global player, playerModels

    # ship randomizer
    if event.keysym == "r":
        s = canvas.coords(player)
        l = len(playerModels)-1
        playerImageRandom = playerModels[randint(0,l)]
        canvas.itemconfig(player, image=playerImageRandom)

    # shoot when space is pressed
    if event.keysym == "space":
        playerShoot(event)

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
    global playerSpeed
    p = canvas.coords(player)
    pWidth = playerImage.width()/2
    pHeight = playerImage.height()/2

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
    if moveStatus[leftBinds] == True and p[0] > pWidth:
        canvas.move(player, -playerSpeed, 0)
    if moveStatus[rightBinds] == True and p[0] < width-pWidth:
        canvas.move(player, playerSpeed, 0)
    if moveStatus[upBinds] == True and p[1] > pHeight:
        canvas.move(player, 0, -playerSpeed)
    if moveStatus[downBinds] == True and p[1] < height-pHeight:
        canvas.move(player, 0, playerSpeed)

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

def playerShoot(event):
    global shotAvailable

    # create box for getting the coords of the ship
    box = canvas.create_rectangle(canvas.bbox(player), outline="")
    c = canvas.coords(box)
    halfX = (c[0] + c[2]) / 2

    if shotAvailable == 1:
        canvas.create_line(halfX,c[1]-30,halfX,c[1],width=4,fill="yellow",tag="shot")
        shotAvailable = 0
        playerShootUpdate("shot")

def playerShootUpdate(name):
    global shotAvailable

    canvas.move(name,0,-playerShootSpeed)
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
        window.after(10, playerShootUpdate, name)

def drawAlien(tag):
    global width, height, alienImage

    alienHeight = alienImage.height()
    randomY = randint(alienHeight, 400)
    randomX = [-100,width+100]
    randomSide = randint(0,1)
    alien = canvas.create_image(randomX[randomSide], randomY, image=alienImage, tag=tag)

    if randomSide == 0:
        alienUpdate(tag, "left")
    elif randomSide == 1:
        alienUpdate(tag, "right")

def alienUpdate(name, side):
    global width, shotAvailable, score

    if side == "left":
        canvas.move(name,7,0)
    elif side == "right":
        canvas.move(name,-7,0)
    canvas.update()
    alienCoords = canvas.coords(name)

    # check if asteroid exists on screen, then execute if true
    if alienCoords:
        if (alienCoords[0] > width and side == "left" or
            alienCoords[0] < 0 and side == "right"):
            canvas.delete(name)
            drawAlien(name)

        # check if asteroid collides with player
        elif isColliding(name, player) == True:
            drawExplosion(name)
            canvas.delete(name)
            updateHealth(-10)
            drawAlien(name)

        # check if asteroid collides with shot
        elif isColliding(name, "shot") == True:
            drawExplosion(name)
            canvas.delete("shot")
            canvas.delete(name)
            shotAvailable = 1
            updateScore(1)
            drawAlien(name)

        else:
            window.after(30, alienUpdate, name, side)

def drawAsteroid(tag):
    global width, height, asteroidImage
    randomX = randint(200, width-200)
    asteroid = canvas.create_image(randomX, -50, image=asteroidImage, tag=tag)
    asteroidUpdate(tag)

def asteroidUpdate(name):
    global height, shotAvailable, score

    canvas.move(name,0,7)
    canvas.update()
    asteroidCoords = canvas.coords(name)

    # check if asteroid exists on screen, then execute if true
    if asteroidCoords:
        if asteroidCoords[1] > height:
            canvas.delete(name)
            drawAsteroid(name)

        # check if asteroid collides with player
        elif isColliding(name, player) == True:
            drawExplosion(name)
            canvas.delete(name)
            updateHealth(-10)
            drawAsteroid(name)

        # check if asteroid collides with shot
        elif isColliding(name, "shot") == True:
            drawExplosion(name)
            canvas.delete("shot")
            canvas.delete(name)
            shotAvailable = 1
            updateScore(1)
            drawAsteroid(name)

        else:
            window.after(30, asteroidUpdate, name)

def drawExplosion(object):
    global explosionImage
    c = canvas.coords(object)
    explosion = canvas.create_image(c[0], c[1], image=explosionImage)
    window.after(250, lambda: canvas.delete(explosion))

def updateScore(amount):
    global score, scoreText, createScoreText
    score += amount
    scoreText = "Score: " + str(score)
    canvas.itemconfig(createScoreText, text=scoreText)

def updateHealth(amount):
    global health, healthText, createHealthText
    health += amount
    healthText = "Health: " + str(health)
    canvas.itemconfig(createHealthText, text=healthText)

def isColliding(object1, object2):
    # see if object1 is an image
    if canvas.bbox(object1):
        a = canvas.create_rectangle(canvas.bbox(object1), outline="")
    else:
        a = object1

    # see if object2 is an image
    if canvas.bbox(object2):
        b = canvas.create_rectangle(canvas.bbox(object2), outline="")
    else:
        b = object2

    x1, y1, x2, y2 = canvas.coords(a)
    result = canvas.find_overlapping(x1, y1, x2, y2)

    if b in result:
        return True
    else:
        return False

def fastShooting(event):
    global isFastShooting, playerShootSpeed, defaultPlayerShootSpeed
    isFastShooting ^= 1

    if isFastShooting == 1:
        playerShootSpeed = 30
    elif isFastShooting == 0:
        playerShootSpeed = defaultPlayerShootSpeed

def fastSpeed(event):
    global isFastSpeed, playerSpeed, defaultPlayerSpeed
    isFastSpeed ^= 1

    if isFastSpeed == 1:
        playerSpeed = 40
    elif isFastSpeed == 0:
        playerSpeed = defaultPlayerSpeed

def bossKey(event):
    global bossKeyToggle, bossKeyLabel, window
    bossKeyToggle ^= 1 # alternate toggle between 1 and 0

    if bossKeyToggle == 1:
        bossKeyLabel.image = bossKeyImage
        bossKeyLabel.place(relx=0.5, rely=0.5, anchor="center")
        window.title("Microsoft Excel - Employees.xlsx")

    elif bossKeyToggle == 0:
        bossKeyLabel.place_forget()
        window.title("Space Shooters")

def setWindowDimensions(w,h):
    window = Tk()
    window.title("Space Shooters")
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
canvas = Canvas(window, width=width, height=height, bg="#2b2b2b", highlightthickness=0)
canvas.pack()

backgroundImage = PhotoImage(file="background.gif").zoom(2)
backgroundLabel = Label(window, image=backgroundImage)
background = canvas.create_image(x, y, image=backgroundImage)

# create the player
playerModels = [PhotoImage(file="ships/ship1.png").subsample(5),
                PhotoImage(file="ships/ship2.png").subsample(7),
                PhotoImage(file="ships/ship3.png").subsample(7)]
playerImage = playerModels[0]
player = canvas.create_image(x, height-100, image=playerImage)

shotAvailable = 1 # set shotAvailable to 1 at beginning of game
defaultPlayerSpeed = 20
defaultPlayerShootSpeed = 10

playerSpeed = defaultPlayerSpeed
playerShootSpeed = defaultPlayerShootSpeed
isFastSpeed = 0
isFastShooting = 0

# aliens
alienModels = [PhotoImage(file="aliens/alien1.png").subsample(9),
               PhotoImage(file="aliens/alien1.gif").subsample(9)]
alienImage = alienModels[0]
drawAlien("alien")

# asteroids
asteroidModels = [PhotoImage(file="asteroids/asteroid1.png").subsample(3)]
asteroidImage = asteroidModels[0]
window.after(1000, lambda: drawAsteroid("asteroid"))

# explosions
explosionModels = [PhotoImage(file="explosion.png").subsample(8)]
explosionImage = explosionModels[0]

# setup boss key
bossKeyToggle = 0
bossKeyImage = PhotoImage(file="misc/bosskey.png")
bossKeyLabel = Label(canvas, image=bossKeyImage, height=height, width=width)

# set score
score = 0
scoreText = "Score: " + str(score)
createScoreText = canvas.create_text(20, 20, anchor=NW, font="terminus 20 bold", text=scoreText, fill="#3a852e")

# set health
health = 100
healthText = "Health: " + str(health)
createHealthText = canvas.create_text(20, 70, anchor=NW, font="terminus 20 bold", text=healthText, fill="#cc272a")

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
window.bind("<Control-f>", fastShooting) # cheat code
window.bind("<Control-s>", fastSpeed) # cheat code

window.mainloop()