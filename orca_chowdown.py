# Orca Chowndown (a 2D Katamari Damacy clone)
# By Daniel I. Kelley and Marie Kelley Daniel.Ian.Kelley@gmail.com
#
# Based on squirrel.py by Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, sys, time, math, pygame
from pygame.locals import *

FPS = 30 # frames per second to update the screen
WINWIDTH = 640 # width of the program's window, in pixels
WINHEIGHT = 480 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

GRASSCOLOR = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

CAMERASLACK = 90     # how far from the center the enemy moves before moving the camera
MOVERATE = 9         # how fast the player moves
BOUNCERATE = 6       # how fast the player bounces (large is slower)
BOUNCEHEIGHT = 30    # how high the player bounces
STARTSIZE = 25       # how big the player starts off
WINSIZE = 300        # how big the player needs to be to win
INVULNTIME = 2       # how long the player is invulnerable after being hit in seconds
MSG_DISPLAY_TIME = 6 # how long the message like "game over" text stays on the screen in seconds
MAXHEALTH = 3        # how much health the player starts with

NUMGRASS = 80        # number of grass objects in the active area
NUM_ENEMIES = 30    # number of enemies in the active area
ENEMY_MINSPEED = 3 # slowest enemy speed
ENEMY_MAXSPEED = 5 # fastest enemy speed
DIRCHANGEFREQ = 2    # % chance of direction change per frame
LEFT = 'left'
RIGHT = 'right'

"""
This program has three data structures to represent the player, enemies, and grass background objects. The data structures are dictionaries with the following keys:

Keys used by all three data structures:
    'x' - the left edge coordinate of the object in the game world (not a pixel coordinate on the screen)
    'y' - the top edge coordinate of the object in the game world (not a pixel coordinate on the screen)
    'rect' - the pygame.Rect object representing where on the screen the object is located.
Player data structure keys:
    'surface' - the pygame.Surface object that stores the image of the Orca which will be drawn to the screen.
    'facing' - either set to LEFT or RIGHT, stores which direction the player is facing.
    'aspect_ratio' - dimension of player image, height / width (The play image width & height are always same aspect ratio)
    'width' - the width of the player in pixels
    'height' - the width of the player in pixels
    'buffer' - helps player eat bigger meals, higher number easier, lower number harder. Recommend keeping around 2.5 to 3 because it gets hard to determine
    'width_apex_predator' - when with achieved turns off buffer and adds bigger enemies
    'bounce' - represents at what point in a bounce the player is in. 0 means standing (no bounce), up to BOUNCERATE (the completion of the bounce)
    'health' - an integer showing how many more times the player can be hit by a larger enemy before dying.
Enemy data structure keys:
    'surface' - the pygame.Surface object that stores the image of the enemy which will be drawn to the screen.
    'movex' - how many pixels per frame the enemy moves horizontally. A negative integer is moving to the left, a positive to the right.
    'movey' - how many pixels per frame the enemy moves vertically. A negative integer is moving up, a positive moving down.
    'width' - the width of the enemy's image, in pixels
    'height' - the height of the enemy's image, in pixels
    'bounce' - represents at what point in a bounce the player is in. 0 means standing (no bounce), up to BOUNCERATE (the completion of the bounce)
    'bouncerate' - how quickly the enemy bounces. A lower number means a quicker bounce.
    'bounceheight' - how high (in pixels) the enemy bounces
Grass data structure keys:
    'grassImage' - an integer that refers to the index of the pygame.Surface object in GRASSIMAGES used for this grass object
"""

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, L_ENEMY_IMG, R_ENEMY_IMG, GRASSIMAGES, L_PLAYER_IMG, R_PLAYER_IMG

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_icon(pygame.image.load('assets/images/gameicon.png'))
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('Orca Chowndown')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)

    # load the image files
    L_ENEMY_IMG = pygame.image.load('assets/images/squid-200x340.png')
    R_ENEMY_IMG = pygame.transform.flip(L_ENEMY_IMG, True, False)

    R_PLAYER_IMG = pygame.image.load('assets/images/orca-425x250.png')
    L_PLAYER_IMG = pygame.transform.flip(R_PLAYER_IMG, True, False)

    GRASSIMAGES = []
    for i in range(1, 5):
        GRASSIMAGES.append(pygame.image.load('assets/images/grass%s.png' % i))

    while True:
        runGame()

def get_image_aspect_ratio(image):
    """Returns the aspect ratio (height / width) of a pygame.Surface image."""
    width = image.get_width()
    height = image.get_height()
    return height / width

def runGame():
    # set up variables for the start of a new game
    invulnerableMode = False  # if the player is invulnerable
    invulnerableStartTime = 0 # time the player became invulnerable
    gameOverMode = False      # if the player has lost
    gameOverStartTime = 0     # time the player lost
    winMode = False           # if the player has won

    # Apex Predator mode
    apexPredatorMode = False
    apexPredatorStartTime = None

    # create the surfaces to hold game text
    gameOverSurfs, gameOverRects = getWrappedGameOverMessage()

    # create the Apex Predator surface
    apexPredatorSurf = BASICFONT.render('You are an Apex Predator!', True, WHITE)
    apexPredatorSurf = apexPredatorSurf.convert_alpha()  # enables alpha transparency
    apexPredatorRect = apexPredatorSurf.get_rect()
    apexPredatorRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT - 50)

    winSurf = BASICFONT.render('You have achieved Final Fin!', True, WHITE)
    winRect = winSurf.get_rect()
    winRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)

    winSurf2 = BASICFONT.render('(Press "r" to restart.)', True, WHITE)
    winRect2 = winSurf2.get_rect()
    winRect2.center = (HALF_WINWIDTH, HALF_WINHEIGHT + 30)

    # camerax and cameray are the top left of where the camera view is
    camerax = 0
    cameray = 0

    grassObjs = []    # stores all the grass objects in the game
    enemyObjs = [] # stores all the non-player enemy objects

    # Calculate dynamically image aspect ratio
    enemyImgAspectRatio = get_image_aspect_ratio(R_ENEMY_IMG)
    playerImgAspectRatio = get_image_aspect_ratio(R_PLAYER_IMG)

    # stores the player object:
    playerObj = {'aspect_ratio': playerImgAspectRatio,
                 'width': STARTSIZE,
                 'height': int(STARTSIZE * playerImgAspectRatio),
                 'surface': pygame.transform.scale(L_PLAYER_IMG, (STARTSIZE, int(STARTSIZE * playerImgAspectRatio))),
                 'facing': LEFT,
                 'buffer': 2.50, # buffer to help player big meals
                 'width_apex_predator': 150, # reduce cheat mode because most meals edible
                 'x': HALF_WINWIDTH,
                 'y': HALF_WINHEIGHT,
                 'bounce':0,
                 'health': MAXHEALTH}

    moveLeft  = False
    moveRight = False
    moveUp    = False
    moveDown  = False

    # start off with some random grass images on the screen
    for i in range(10):
        grassObjs.append(makeNewGrass(camerax, cameray))
        grassObjs[i]['x'] = random.randint(0, WINWIDTH)
        grassObjs[i]['y'] = random.randint(0, WINHEIGHT)

    while True: # main game loop
        # Check if we should turn off invulnerability
        if invulnerableMode and time.time() - invulnerableStartTime > INVULNTIME:
            invulnerableMode = False

        # move all the enemies
        for sObj in enemyObjs:
            # move the enemy, and adjust for their bounce
            sObj['x'] += sObj['movex']
            sObj['y'] += sObj['movey']
            sObj['bounce'] += 1
            if sObj['bounce'] > sObj['bouncerate']:
                sObj['bounce'] = 0 # reset bounce amount

            # random chance they change direction
            if random.randint(0, 99) < DIRCHANGEFREQ:
                sObj['movex'] = getRandomVelocity()
                sObj['movey'] = getRandomVelocity()
                if sObj['movex'] > 0: # faces right
                    sObj['surface'] = pygame.transform.scale(R_ENEMY_IMG, (sObj['width'], sObj['height']))
                else: # faces left
                    sObj['surface'] = pygame.transform.scale(L_ENEMY_IMG, (sObj['width'], sObj['height']))


        # go through all the objects and see if any need to be deleted.
        for i in range(len(grassObjs) - 1, -1, -1):
            if isOutsideActiveArea(camerax, cameray, grassObjs[i]):
                del grassObjs[i]
        for i in range(len(enemyObjs) - 1, -1, -1):
            if isOutsideActiveArea(camerax, cameray, enemyObjs[i]):
                del enemyObjs[i]

        # add more grass & enemies if we don't have enough.
        while len(grassObjs) < NUMGRASS:
            grassObjs.append(makeNewGrass(camerax, cameray))
        while len(enemyObjs) < NUM_ENEMIES:
            enemyObjs.append(makeNewSquid(camerax, cameray, enemyImgAspectRatio, apexPredatorMode))

        # adjust camerax and cameray if beyond the "camera slack"
        playerCenterx = playerObj['x'] + int(playerObj['width'] / 2)
        playerCentery = playerObj['y'] + int(playerObj['height'] / 2)
        if (camerax + HALF_WINWIDTH) - playerCenterx > CAMERASLACK:
            camerax = playerCenterx + CAMERASLACK - HALF_WINWIDTH
        elif playerCenterx - (camerax + HALF_WINWIDTH) > CAMERASLACK:
            camerax = playerCenterx - CAMERASLACK - HALF_WINWIDTH
        if (cameray + HALF_WINHEIGHT) - playerCentery > CAMERASLACK:
            cameray = playerCentery + CAMERASLACK - HALF_WINHEIGHT
        elif playerCentery - (cameray + HALF_WINHEIGHT) > CAMERASLACK:
            cameray = playerCentery - CAMERASLACK - HALF_WINHEIGHT

        # draw the green background
        DISPLAYSURF.fill(GRASSCOLOR)

        # draw all the grass objects on the screen
        for gObj in grassObjs:
            gRect = pygame.Rect( (gObj['x'] - camerax,
                                  gObj['y'] - cameray,
                                  gObj['width'],
                                  gObj['height']) )
            DISPLAYSURF.blit(GRASSIMAGES[gObj['grassImage']], gRect)


        # draw the other enemies
        for sObj in enemyObjs:
            sObj['rect'] = pygame.Rect( (sObj['x'] - camerax,
                                         sObj['y'] - cameray - getBounceAmount(sObj['bounce'], sObj['bouncerate'], sObj['bounceheight']),
                                         sObj['width'],
                                         sObj['height']) )
            DISPLAYSURF.blit(sObj['surface'], sObj['rect'])


        # draw the player
        flashIsOn = round(time.time(), 1) * 10 % 2 == 1
        if not gameOverMode and not (invulnerableMode and flashIsOn):
            playerObj['rect'] = pygame.Rect( (playerObj['x'] - camerax,
                                            playerObj['y'] - cameray - getBounceAmount(playerObj['bounce'], BOUNCERATE, BOUNCEHEIGHT),
                                            playerObj['width'],
                                            playerObj['height']) )
            DISPLAYSURF.blit(playerObj['surface'], playerObj['rect'])


        # draw the health meter
        drawHealthMeter(playerObj['health'])

        for event in pygame.event.get(): # event handling loop
            if event.type == pygame.QUIT:
                terminate()

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    moveDown = False
                    moveUp = True
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    moveUp = False
                    moveDown = True
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    moveRight = False
                    moveLeft = True
                    if playerObj['facing'] != LEFT: # change player image
                        playerObj['surface'] = pygame.transform.scale(L_PLAYER_IMG, (playerObj['width'], playerObj['height']))
                    playerObj['facing'] = LEFT
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    moveLeft = False
                    moveRight = True
                    if playerObj['facing'] != RIGHT: # change player image
                        playerObj['surface'] = pygame.transform.scale(R_PLAYER_IMG, (playerObj['width'], playerObj['height']))
                    playerObj['facing'] = RIGHT
                elif winMode and event.key == pygame.K_r:
                    return

            elif event.type == pygame.KEYUP:
                # stop moving the player
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    moveLeft = False
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    moveRight = False
                elif event.key in (pygame.K_UP, pygame.K_w):
                    moveUp = False
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    moveDown = False

                elif event.key == pygame.K_ESCAPE:
                    terminate()

        if not gameOverMode:
            # actually move the player
            if moveLeft:
                playerObj['x'] -= MOVERATE
            if moveRight:
                playerObj['x'] += MOVERATE
            if moveUp:
                playerObj['y'] -= MOVERATE
            if moveDown:
                playerObj['y'] += MOVERATE

            if (moveLeft or moveRight or moveUp or moveDown) or playerObj['bounce'] != 0:
                playerObj['bounce'] += 1

            if playerObj['bounce'] > BOUNCERATE:
                playerObj['bounce'] = 0 # reset bounce amount

            # check if the player has collided with any enemies
            for i in range(len(enemyObjs)-1, -1, -1):
                sqObj = enemyObjs[i]
                if 'rect' in sqObj and playerObj['rect'].colliderect(sqObj['rect']):
                    # a player/enemy collision has occurred

                    if sqObj['width'] * sqObj['height'] <= playerObj['width'] * playerObj['height'] * playerObj['buffer']:
                        # player is larger and eats the enemy
                        playerObj['width'] += int( (sqObj['width'] * sqObj['height'])**0.2 ) + 1
                        playerObj['height'] = int(playerObj['width'] * playerObj['aspect_ratio'])

                        # Reduce buffer to 1.0 once player is large enough to eat most meals
                        if playerObj['width'] >= playerObj['width_apex_predator'] and not apexPredatorMode:
                            playerObj['buffer'] = 1.0
                            apexPredatorMode = True
                            apexPredatorStartTime = time.time()
                            print("Buffer reduced to 1.0 - you're now an apex predator!")

                        del enemyObjs[i]

                        if playerObj['facing'] == LEFT:
                            playerObj['surface'] = pygame.transform.scale(L_PLAYER_IMG, (playerObj['width'], playerObj['height']))
                        else:
                            playerObj['surface'] = pygame.transform.scale(R_PLAYER_IMG, (playerObj['width'], playerObj['height']))

                        if playerObj['width'] > WINSIZE:
                            winMode = True # turn on "win mode"

                    elif not invulnerableMode:
                        # player is smaller and takes damage
                        invulnerableMode = True
                        invulnerableStartTime = time.time()
                        playerObj['health'] -= 1
                        if playerObj['health'] == 0:
                            gameOverMode = True # turn on "game over mode"
                            gameOverStartTime = time.time()
        else:
            # game is over, show "game over" text
            for i in range(len(gameOverSurfs)):
                DISPLAYSURF.blit(gameOverSurfs[i], gameOverRects[i])
            if time.time() - gameOverStartTime > MSG_DISPLAY_TIME:
                return # end the current game

        # check if the player has won.
        if winMode:
            DISPLAYSURF.blit(winSurf, winRect)
            DISPLAYSURF.blit(winSurf2, winRect2)

        # Show Apex Predator message with fade-out
        if apexPredatorMode and apexPredatorStartTime:
            elapsed = time.time() - apexPredatorStartTime
            if elapsed <= MSG_DISPLAY_TIME:
                alpha = max(0, int(255 * (1 - elapsed / MSG_DISPLAY_TIME)))  # fade from 255 to 0
                tempSurf = apexPredatorSurf.copy()
                tempSurf.set_alpha(alpha)
                DISPLAYSURF.blit(tempSurf, apexPredatorRect)

        pygame.display.update()
        FPSCLOCK.tick(FPS)




def drawHealthMeter(currentHealth):
    for i in range(currentHealth): # draw red health bars
        pygame.draw.rect(DISPLAYSURF, RED,   (15, 5 + (10 * MAXHEALTH) - i * 10, 20, 10))
    for i in range(MAXHEALTH): # draw the white outlines
        pygame.draw.rect(DISPLAYSURF, WHITE, (15, 5 + (10 * MAXHEALTH) - i * 10, 20, 10), 1)


def terminate():
    pygame.quit()
    sys.exit()


def getBounceAmount(currentBounce, bounceRate, bounceHeight):
    # Returns the number of pixels to offset based on the bounce.
    # Larger bounceRate means a slower bounce.
    # Larger bounceHeight means a higher bounce.
    # currentBounce will always be less than bounceRate
    return int(math.sin( (math.pi / float(bounceRate)) * currentBounce ) * bounceHeight)

def getRandomVelocity():
    speed = random.randint(ENEMY_MINSPEED, ENEMY_MAXSPEED)
    if random.randint(0, 1) == 0:
        return speed
    else:
        return -speed


def getRandomOffCameraPos(camerax, cameray, objWidth, objHeight):
    # create a Rect of the camera view
    cameraRect = pygame.Rect(camerax, cameray, WINWIDTH, WINHEIGHT)
    while True:
        x = random.randint(camerax - WINWIDTH, camerax + (2 * WINWIDTH))
        y = random.randint(cameray - WINHEIGHT, cameray + (2 * WINHEIGHT))
        # create a Rect object with the random coordinates and use colliderect()
        # to make sure the right edge isn't in the camera view.
        objRect = pygame.Rect(x, y, objWidth, objHeight)
        if not objRect.colliderect(cameraRect):
            return x, y


def makeNewSquid(camerax, cameray, imgAspectRatio, apexPredatorMode=False):
    sq = {}
    if apexPredatorMode:
        generalSize = random.randint(15, 40)
        multiplier = random.randint(2, 4)
    else:
        generalSize = random.randint(5, 25)
        multiplier = random.randint(1, 3)

    base_width = (generalSize + random.randint(0, 10)) * multiplier
    sq['width'] = base_width
    sq['height'] = int(base_width * imgAspectRatio) # keep original enemy image ratio (height / width)
    sq['x'], sq['y'] = getRandomOffCameraPos(camerax, cameray, sq['width'], sq['height'])
    sq['movex'] = getRandomVelocity()
    sq['movey'] = getRandomVelocity()
    if sq['movex'] < 0: # enemy is facing left
        sq['surface'] = pygame.transform.scale(L_ENEMY_IMG, (sq['width'], sq['height']))
    else: # enemy is facing right
        sq['surface'] = pygame.transform.scale(R_ENEMY_IMG, (sq['width'], sq['height']))
    sq['bounce'] = 0
    sq['bouncerate'] = random.randint(10, 18)
    sq['bounceheight'] = random.randint(10, 50)
    return sq


def makeNewGrass(camerax, cameray):
    gr = {}
    gr['grassImage'] = random.randint(0, len(GRASSIMAGES) - 1)
    gr['width']  = GRASSIMAGES[0].get_width()
    gr['height'] = GRASSIMAGES[0].get_height()
    gr['x'], gr['y'] = getRandomOffCameraPos(camerax, cameray, gr['width'], gr['height'])
    gr['rect'] = pygame.Rect( (gr['x'], gr['y'], gr['width'], gr['height']) )
    return gr


def isOutsideActiveArea(camerax, cameray, obj):
    # Return False if camerax and cameray are more than
    # a half-window length beyond the edge of the window.
    boundsLeftEdge = camerax - WINWIDTH
    boundsTopEdge = cameray - WINHEIGHT
    boundsRect = pygame.Rect(boundsLeftEdge, boundsTopEdge, WINWIDTH * 3, WINHEIGHT * 3)
    objRect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
    return not boundsRect.colliderect(objRect)

def wrap_text(text, font, max_width):
    """Wrap text into lines that fit within max_width when rendered with the font."""
    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + ' '
    lines.append(current_line.strip())
    return lines

def getWrappedGameOverMessage():
    """Randomly selects and wraps a game over message, returning rendered surfaces and their rects."""

    # create the surfaces to hold game text
    gameOverMessages = [
        "Game Over - You've sunken into the Abyss.",
        "Game Over - The squids vanished... and took your dignity with them.",
        "Game Over - Inked, outflanked, and outwitted.",
        "Game Over - You dove too deep. The squids were waiting.",
        "Game Over - Tentacles tighten. The deep claims another.",
        "Game Over - One orca vs a thousand arms? Bad odds.",
        "Game Over - The squids inked a masterpiece… and you were the canvas.",
        "Game Over - Their minds were alien. Their strategy, flawless.",
        "Game Over - Drenched in ink and regret.",
        "Game Over - You were the apex predator... until you weren't.",
        "Game Over - The squids coordinated. You hesitated."
    ]

    # Pick a message and wrap it
    chosenGameOverMsg = random.choice(gameOverMessages)
    wrappedLines = wrap_text(chosenGameOverMsg, BASICFONT, WINWIDTH - 40)  # leave some margin

    # Render each line into a surface
    surfaces = [BASICFONT.render(line, True, WHITE) for line in wrappedLines]
    rects = [surf.get_rect() for surf in surfaces]

    # Center all lines vertically around HALF_WINHEIGHT
    total_height = sum(rect.height for rect in rects) + (len(rects) - 1) * 5  # add spacing
    start_y = HALF_WINHEIGHT - total_height // 2

    for rect in rects:
        rect.centerx = HALF_WINWIDTH

    # Apply vertical positioning
    for i, rect in enumerate(rects):
        rect.top = start_y + i * (rect.height + 5)

    return surfaces, rects

if __name__ == '__main__':
    main()