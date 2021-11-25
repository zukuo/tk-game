from tkinter import *
from random import randint
import json

# set the screen size/resolution here
width = 1600
height = 900

def playerControls(event):
    global player, playerModels

    # ship randomiser / cheat code
    if event.keysym == "r":
        l = len(playerModels)-1
        playerImageRandom = playerModels[randint(0,l)]
        canvas.itemconfig(player, image=playerImageRandom)

    # shoot when space is pressed
    if event.keysym == "space" and isPaused == 0:
        playerShoot(event)

    # pause game on escape
    if event.keysym == "Escape":
        pauseGame()

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

    if isPaused == 0:
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

    if isPaused == 0:
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

def drawAlien(tag, model):
    global width, height, alienImage

    alienImage = alienModels[model]
    alienHeight = alienImage.height()
    randomY = randint(alienHeight, 350)
    randomX = [-100,width+100]
    randomSide = randint(0,1)
    alien = canvas.create_image(randomX[randomSide], randomY, image=alienImage, tag=tag)

    if randomSide == 0:
        alienUpdate(tag, "left", model)
    elif randomSide == 1:
        alienUpdate(tag, "right", model)

def alienUpdate(name, side, model):
    global width, shotAvailable, score

    alienCoords = canvas.coords(name)

    if isPaused == 0:
        if side == "left":
            canvas.move(name,7,0)
        elif side == "right":
            canvas.move(name,-7,0)
        canvas.update()

    # check if asteroid exists on screen, then execute if true
    if alienCoords:
        if (alienCoords[0] > width and side == "left" or
            alienCoords[0] < 0 and side == "right"):
            canvas.delete(name)
            drawAlien(name, model)

        # check if asteroid collides with player
        elif isColliding(name, player) == True:
            drawExplosion(name)
            canvas.delete(name)
            updateHealth(-15)
            drawAlien(name, model)

        # check if asteroid collides with shot
        elif isColliding(name, "shot") == True:
            drawExplosion(name)
            canvas.delete("shot")
            canvas.delete(name)
            shotAvailable = 1
            updateScore(5)
            drawAlien(name, model)

        else:
            alienLoop = window.after(30, alienUpdate, name, side, model)
    
    if isPaused == 0:
        checkHealth()

def drawAlienMenu(tag):
    global width, height, alienImage

    alienHeight = alienImage.height()
    randomY = randint(alienHeight, 175)
    randomX = [-100,width+100]
    randomSide = randint(0,1)
    alien = menuCanvas.create_image(randomX[randomSide], randomY, image=alienImage, tag=tag)

    if randomSide == 0:
        alienUpdateMenu(tag, "left")
    elif randomSide == 1:
        alienUpdateMenu(tag, "right")

def alienUpdateMenu(name, side):
    global width, shotAvailable, score, menuCanvas

    if menuCanvas.winfo_exists():
        if side == "left":
            menuCanvas.move(name,7,0)
        elif side == "right":
            menuCanvas.move(name,-7,0)
        menuCanvas.update()

        if menuCanvas.coords(name):
            alienCoords = menuCanvas.coords(name)

    if menuCanvas.winfo_exists():
        # check if asteroid exists on screen, then execute if true
        if alienCoords:
            if (alienCoords[0] > width and side == "left" or
                alienCoords[0] < 0 and side == "right"):
                menuCanvas.delete(name)
                drawAlienMenu(name)
            else:
                window.after(30, alienUpdateMenu, name, side)

def drawAsteroid(tag):
    global width, height, asteroidImage
    randomX = randint(200, width-200)
    asteroid = canvas.create_image(randomX, -200, image=asteroidImage, tag=tag)
    asteroidUpdate(tag)

def asteroidUpdate(name):
    global height, shotAvailable, score

    asteroidCoords = canvas.coords(name)

    if isPaused == 0:
        canvas.move(name,0,7)
        canvas.update()

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
            asteroidLoop = window.after(30, asteroidUpdate, name)

    if isPaused == 0:
        checkHealth()

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

def checkHealth():
    global health
    if health <= 0:
        gameOver()

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

    if canvas.coords(a):
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

def selectCharacter(num):
    global playerImage
    playerImage = playerModels[num]
    canvas.itemconfig(player, image=playerImage)

def updateName(enteredName):
    global name
    name = enteredName

def mainMenu():
    global menuCanvas, active
    if not menuCanvas.winfo_exists():
        menuCanvas = Canvas(window, width=width, height=height, bg="#2b2b2b", highlightthickness=0)
        if settingsCanvas.winfo_exists():
            settingsCanvas.destroy()
        if leaderCanvas.winfo_exists():
            leaderCanvas.destroy()
        if gameOverCanvas.winfo_exists():
            gameOverCanvas.destroy()
        if timeUpCanvas.winfo_exists():
            timeUpCanvas.destroy()

    menuBackground = menuCanvas.create_image(x, y, image=menuBackgroundImage)
    alienMenuLoop = menuCanvas.after(250, lambda: drawAlienMenu("menuAlien"))
    logo = menuCanvas.create_image(x, y-140, image=logoImage)
    active = "#0BB93B"

    startButton = Button(window, text="Start", command=startGame, anchor=CENTER)
    startButton.configure(fg=front, bg=back, width=10, activebackground=active)
    startButtonWindow = menuCanvas.create_window(x, y, anchor=CENTER, window=startButton)

    leaderButton = Button(window, text="Leaderboard", command=leaderMenu, anchor=CENTER)
    leaderButton.configure(fg=front, bg=back, width=10, activebackground=active)
    leaderButtonWindow = menuCanvas.create_window(x, y+50, anchor=CENTER, window=leaderButton)

    settingsButton = Button(window, text="Settings", command=settingsMenu, anchor=CENTER)
    settingsButton.configure(fg=front, bg=back, width=10, activebackground=active)
    settingsButtonWindow = menuCanvas.create_window(x, y+100, anchor=CENTER, window=settingsButton)

    quitButton = Button(window, text="Quit", command=quit, anchor=CENTER)
    quitButton.configure(fg=front, bg=back, width=10, activebackground=active)
    quitButtonWindow = menuCanvas.create_window(x, y+150, anchor=CENTER, window=quitButton)

    menuCanvas.pack()

def settingsMenu():
    global settingsCanvas, active
    if not settingsCanvas.winfo_exists():
        settingsCanvas = Canvas(window, width=width, height=height, bg="#2b2b2b", highlightthickness=0)
    menuCanvas.destroy()
    menuBackground = settingsCanvas.create_image(x, y, image=menuBackgroundImage)
    logo = settingsCanvas.create_image(x, y-250, image=settingsImage)
    active = "#DC6700"

    difficultyText = settingsCanvas.create_text(x, y-150,text="Choose a Difficulty:", fill="white")

    playerText = settingsCanvas.create_text(x, y-90,text="Choose a Ship:", fill="white")

    r1 = Radiobutton(window, image=playerModels[0], value=0)
    r1.configure(fg=front, bg=back, activebackground=active, selectcolor=active,
                 command=lambda: selectCharacter(0), indicatoron = 0)
    r1Window = settingsCanvas.create_window(x, y, anchor=CENTER, window=r1)

    r2 = Radiobutton(window, image=playerModels[1], value=1)
    r2.configure(fg=front, bg=back, activebackground=active, selectcolor=active,
                 command=lambda: selectCharacter(1), indicatoron = 0)
    r2Window = settingsCanvas.create_window(x+150, y, anchor=CENTER, window=r2)

    r3 = Radiobutton(window, image=playerModels[2], value=2)
    r3.configure(fg=front, bg=back, activebackground=active, selectcolor=active,
                 command=lambda: selectCharacter(2), indicatoron = 0)
    r3Window = settingsCanvas.create_window(x-150, y, anchor=CENTER, window=r3)

    nameText = settingsCanvas.create_text(x, y+110,text="Your Name:", fill="white")
    nameEntry = Entry(window)
    nameEntry.configure(fg=front, bg=back, width=15)
    nameEntryWindow = settingsCanvas.create_window(x, y+140, anchor=CENTER, window=nameEntry)

    nameButton = Button(window, text="Submit", anchor=CENTER)
    nameButton.configure(fg=front, bg=back, width=5, activebackground=active,
                         command=lambda: updateName(nameEntry.get()))
    nameButtonWindow = settingsCanvas.create_window(x, y+180, anchor=CENTER, window=nameButton)
    
    quitButton = Button(window, text="Return to Menu", command=mainMenu, anchor=CENTER)
    quitButton.configure(fg=front, bg=back, width=11, activebackground=active)
    quitButtonWindow = settingsCanvas.create_window(x, y+240, anchor=CENTER, window=quitButton)

    settingsCanvas.pack()

def leaderMenu():
    global leaderCanvas, active
    if not leaderCanvas.winfo_exists():
        leaderCanvas = Canvas(window, width=width, height=height, bg="#2b2b2b", highlightthickness=0)
    menuCanvas.destroy()
    menuBackground = leaderCanvas.create_image(x, y, image=menuBackgroundImage)
    leader = leaderCanvas.create_image(x, y-250, image=leaderImage)
    active = "#0B93C6"
    createLeader()

    quitButton = Button(window, text="Return to Menu", command=mainMenu, anchor=CENTER)
    quitButton.configure(fg=front, bg=back, width=11, activebackground=active)
    quitButtonWindow = leaderCanvas.create_window(x, y+250, anchor=CENTER, window=quitButton)

    leaderCanvas.pack()

def startGame():
    global canvas

    # if game canvas (from before) does not exist re-instantiate everything
    if not canvas.winfo_exists():
        canvas = Canvas(window, width=width, height=height, bg="#2b2b2b", highlightthickness=0)
    menuCanvas.destroy()

    # create objects inside game canvas
    canvas.pack()
    gameTimer()
    window.after(1000, lambda: drawAlien("alien1", 0))
    window.after(2000, lambda: drawAlien("alien2", 1))
    window.after(500, lambda: drawAsteroid("asteroid1"))
    window.after(1500, lambda: drawAsteroid("asteroid2"))

def instantiateGame():
    global health, score, shotAvailable, canvas, isPaused
    canvas = Canvas(window, width=width, height=height, bg="#2b2b2b", highlightthickness=0)
    health = defaultHealth
    score = defaultScore
    shotAvailable = 1
    isPaused = 0
    healthText = "Health: " + str(health)
    scoreText = "Score: " + str(score)

    background = canvas.create_image(x, y, image=backgroundImage)
    player = canvas.create_image(x, height-100, image=playerImage)
    createScoreText = canvas.create_text(20, 20, anchor=NW, font="sans 20 bold", text=scoreText, fill="#3a852e")
    createHealthText = canvas.create_text(20, 70, anchor=NW, font="sans 20 bold", text=healthText, fill="#cc272a")

def gameOver():
    global gameOverCanvas, active
    if not gameOverCanvas.winfo_exists():
        gameOverCanvas = Canvas(window, width=width, height=height, bg="#2b2b2b", highlightthickness=0)
    if gameOverCanvas.winfo_exists():
        canvas.destroy()

    active = "#D22929"
    background = gameOverCanvas.create_image(x, y, image=backgroundImage)
    gameOverCanvas.create_image(x, y-100, image=gameOverImage)

    nameText = "You Died, Nice Try!"
    finalScoreText = "Your final score was: " + str(score)
    gameOverCanvas.create_text(x, y+50, font="sans 20 bold", text=nameText, fill=active)
    gameOverCanvas.create_text(x, y+100, font="sans 20 bold", text=finalScoreText, fill=active)

    nameText = gameOverCanvas.create_text(x, y+150,text="Your Name:", fill="white")
    nameEntry = Entry(window)
    nameEntry.configure(fg=front, bg=back, width=15)
    nameEntryWindow = gameOverCanvas.create_window(x, y+180, anchor=CENTER, window=nameEntry)

    updatedScore = score
    nameButton = Button(window, text="Submit", anchor=CENTER)
    nameButton.configure(fg=front, bg=back, width=5, activebackground=active,
                         command=lambda: updateScoreData(nameEntry.get(), updatedScore))
    nameButtonWindow = gameOverCanvas.create_window(x, y+220, anchor=CENTER, window=nameButton)

    quitButton = Button(window, text="Return to Menu", command=mainMenu, anchor=CENTER)
    quitButton.configure(fg=front, bg=back, width=11, activebackground=active)
    quitButtonWindow = gameOverCanvas.create_window(x, y+280, anchor=CENTER, window=quitButton)

    instantiateGame()
    gameOverCanvas.pack()

def pauseGame():
    global isPaused, pause
    if bossKeyToggle == 0:
        isPaused ^= 1
        if isPaused == 1:
            pause = canvas.create_image(x, y, image=pauseImage)
        if isPaused == 0:
            canvas.delete(pause)

def timeUp():
    global timeUpCanvas, active
    if not timeUpCanvas.winfo_exists():
        timeUpCanvas = Canvas(window, width=width, height=height, bg="#2b2b2b", highlightthickness=0)
    if timeUpCanvas.winfo_exists():
        canvas.destroy()

    active = "#FF5200"
    background = timeUpCanvas.create_image(x, y, image=backgroundImage)
    timeUpCanvas.create_image(x, y-100, image=timeUpImage)

    nameText = "Well Done!"
    finalScoreText = "Your final score was: " + str(score)
    timeUpCanvas.create_text(x, y+50, font="sans 20 bold", text=nameText, fill=active)
    timeUpCanvas.create_text(x, y+100, font="sans 20 bold", text=finalScoreText, fill=active)

    nameText = timeUpCanvas.create_text(x, y+150,text="Your Name:", fill="white")
    nameEntry = Entry(window)
    nameEntry.configure(fg=front, bg=back, width=15)
    nameEntryWindow = timeUpCanvas.create_window(x, y+180, anchor=CENTER, window=nameEntry)

    updatedScore = score
    nameButton = Button(window, text="Submit", anchor=CENTER)
    nameButton.configure(fg=front, bg=back, width=5, activebackground=active,
                         command=lambda: updateScoreData(nameEntry.get(), updatedScore))
    nameButtonWindow = timeUpCanvas.create_window(x, y+220, anchor=CENTER, window=nameButton)

    quitButton = Button(window, text="Return to Menu", command=mainMenu, anchor=CENTER)
    quitButton.configure(fg=front, bg=back, width=11, activebackground=active)
    quitButtonWindow = timeUpCanvas.create_window(x, y+280, anchor=CENTER, window=quitButton)

    instantiateGame()
    timeUpCanvas.pack()

def gameTimer():
    global timer, createTimerText
    timer = defaultTime
    createTimerText = canvas.create_text(x, 60, font="sans 20 bold", text=timer, fill="white")
    updateTimer()

def updateTimer():
    global timer, timerCoords
    timerCoords = canvas.coords(createTimerText)
    if timerCoords:
        if isPaused == 0:
            canvas.itemconfig(createTimerText, text=timer)
            timer -= 1
        timerLoop = window.after(1000, updateTimer)

    # using -2 to prevent visual bug, due to after delay
    if timer <= -2 and isPaused == 0 and timerCoords:
        timeUp()

def updateScoreData(playerName, newScore):
    scores[playerName.title()] = newScore
    with open(scoreFile, 'w+') as f:
        json.dump(scores, f, sort_keys=True, indent=2)

def createLeader():
    scoresSorted = sorted([(player, score) for player, score in scores.items()], reverse=True, key=lambda x: x[1])
    i = 1
    j = -160
    for p, s in scoresSorted:
        if i > 10: # only show top 10
            break
        leaderText = str(i) + ". " + p + " - " + str(s)
        leaderCanvas.create_text(x, y+j, text=leaderText, font="sans 15 bold", fill="white")
        j += 40
        i += 1

def bossKey(event):
    global bossKeyToggle, bossKeyLabel, window, isPaused
    bossKeyToggle ^= 1 # alternate toggle between 1 and 0
    isPaused ^= 1

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

# setup game canvas
x = width / 2
y = height / 2
window = setWindowDimensions(width, height)
canvas = Canvas(window, width=width, height=height, bg="#2b2b2b", highlightthickness=0)

# setup main menu system
logoImage = PhotoImage(file="misc/logo.png")
settingsImage = PhotoImage(file="misc/settings.png")
leaderImage = PhotoImage(file="misc/leader.png")
menuBackgroundImage = PhotoImage(file="misc/menuback.png")

menuCanvas = Canvas(window, width=width, height=height, bg="#2b2b2b", highlightthickness=0)
settingsCanvas = Canvas(window, width=width, height=height, bg="#2b2b2b", highlightthickness=0)
leaderCanvas = Canvas(window, width=width, height=height, bg="#2b2b2b", highlightthickness=0)

active = "#0BB93B"
front = "#FFFFFF"
back = "#3b3b3b"

# setup game over system
gameOverImage = PhotoImage(file="misc/gameover.png")
gameOverCanvas = Canvas(window, width=width, height=height, bg="#2b2b2b", highlightthickness=0)

# set background image
backgroundImage = PhotoImage(file="misc/background.gif").zoom(2)
background = canvas.create_image(x, y, image=backgroundImage)

# create the player
playerModels = [PhotoImage(file="ships/ship1.png").subsample(5),
                PhotoImage(file="ships/ship2.png").subsample(7),
                PhotoImage(file="ships/ship3.png").subsample(7)]
playerImage = playerModels[0]
player = canvas.create_image(x, height-100, image=playerImage)
name = "player"

shotAvailable = 1 # set shotAvailable to 1 at beginning of game
defaultPlayerSpeed = 20
defaultPlayerShootSpeed = 10

playerSpeed = defaultPlayerSpeed
playerShootSpeed = defaultPlayerShootSpeed
isFastSpeed = 0
isFastShooting = 0

# leaderboard scores
scoreFile = r"data/scores.json"
try:
    with open(scoreFile, 'r') as f:
        scores = json.load(f)
except FileNotFoundError:
    scores = {}

# aliens
alienModels = [PhotoImage(file="aliens/alien1.png").subsample(9),
               PhotoImage(file="aliens/alien2.png").subsample(7)]
alienImage = alienModels[0]

# asteroids
asteroidModels = [PhotoImage(file="asteroids/asteroid1.png").subsample(3)]
asteroidImage = asteroidModels[0]

# explosions
explosionModels = [PhotoImage(file="misc/explosion.png").subsample(8)]
explosionImage = explosionModels[0]

# setup boss key
bossKeyToggle = 0
bossKeyImage = PhotoImage(file="misc/bosskey.png")
bossKeyLabel = Label(window, image=bossKeyImage, height=height, width=width, bg=None)

# setup pause system
pauseImage = PhotoImage(file="misc/pause.png")
isPaused = 0

# setup timer
timeUpImage = PhotoImage(file="misc/timeup.png")
timeUpCanvas = Canvas(window, width=width, height=height, bg="#2b2b2b", highlightthickness=0)
defaultTime = 5
timer = defaultTime

# set score
defaultScore = 0
score = defaultScore
scoreText = "Score: " + str(score)
createScoreText = canvas.create_text(20, 20, anchor=NW, font="sans 20 bold", text=scoreText, fill="#3a852e")

# set health
defaultHealth = 10
health = defaultHealth
healthText = "Health: " + str(health)
createHealthText = canvas.create_text(20, 70, anchor=NW, font="sans 20 bold", text=healthText, fill="#cc272a")

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

mainMenu()

window.mainloop()