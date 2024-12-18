#something like this:
#https://rhythmdr.com/cny/

"""
stuff i used

sys.stdout is just fancy print. idk

sys.stdout.write("\033[F") this command tells the print thing to move up one. |
sys.stdout.write("\033[3F") this moves it up 3 times

sys.stdout.write("\033[K") this command clears the current line

"""

import time
import threading
import sys
import pygame
from game import Game

pygame.init()
screen = pygame.display.set_mode((600, 500))
clock = pygame.time.Clock()

game = Game('img/column3.png', 'img/cursor.png', 'img/background2.jpg')
game.resize_images()




#how many seconds after program runs to start a 7 thing. //
#how many seconds between beats for the 7 hit above thingy
#samurai techno is 200 bpm. .6 for fast, .3 for medium, .15 for fast
LEVEL_BPM = 200
LEVEL_SECONDS_PER_BEAT = 60/LEVEL_BPM
#LEVEL_HITS_BEAT        = [0, 32, 48, 51.16, 59.16]
#LEVEL_HITS_TIMING_BEAT = [4, 2,  1, .5,    .5]
#                                                                                the drop V                                                                                                                                   #slowdown V
LEVEL_HITS        = [0,    9.6, 14.4, 16.55, 17.75, 19.25, 21.65, 24.05, 26.15, 27.35, 28.8, 30,  31.2, 32.4, 33.6, 34.8, 36,  37.2, 38.4, 39.6, 40.8, 42,  43.2, 44.4, 45.6, 46.8, 48,  49.2, 50.4, 51.6, 52.8, 54,  55.2, 56.4, 57.6, 58.95, 60,  61.35,  62.4,  63.75, 64.8, 65.85, 67.05, 68.25, 72.3]
LEVEL_HITS_TIMING = [1.2, .6,  .3,   .15,   .15,   .3,   .3,   .3,      .15,   .15,   .15,  .15, .15,  .15,  .15,  .15,  .15, .15,  .15,  .15,  .15,  .15, .15,  .15,  .15,  .15,  .15, .15,  .15,  .15,  .15,  .15, .15,  .15,  .15,  .15,   .15, .15,    .15,   .15,   .15,  .15,   .15,   .15,   .15]
LEVEL_END = 74 #what time to end the level
LEVEL_END = 5


LEVEL_ACTUAL_HITS = [] # timing of when they actually have to hit


leniency = .15 #if hit is within this many seconds (+-) of a valid input then allow it
hitOffset = 0 #offset for hit after beat
beatOffset = 0.05 #offset for beat in relation to music
#secondsPerBeat = .5 #how many seconds are in each "beat" of the song. replaced with levelhitstiming
goodHits = 0 #how many times player got a good hit
badHits = 0 #how many times player missed a note
levelIndex = 0 #what hit the program is on
playerIndex = 0 #what hit the player is on (this should always be lower than or equal to levelindex)
accuracyList = [] #list of offsets
checkNewBeat = False
globalFeedback = "Press space on the 7th beat"


#start = time.time() # set up the time at the start


for i in range(len(LEVEL_HITS)):
    LEVEL_ACTUAL_HITS.append(LEVEL_HITS[i] + LEVEL_HITS_TIMING[i]*6 + beatOffset)

        
game.show_background(screen)
game.show_colums(screen)

def getRuntime(): # this function returns how much time since the program started (useful for getting time on the level)
    return time.time() - game.startTime

def getOffset(time): #this function returns how off you were in ms
    return int((getRuntime() - time - hitOffset)*1000)


def drawScreen():
    global goodHits, badHits
    red = (100, 0, 5)
    teal = (0, 244, 207)
    font = pygame.font.Font('freesansbold.ttf', 16)

    game.show_background(screen)
    screen.blit((font.render("Follow the music", True, (104, 104, 227))), (25, 25))
    screen.blit((font.render("Press space on the 7th beat", True, (227, 188, 104))), (25, 50))
    teal = (0, 244, 207)
    font = pygame.font.Font('freesansbold.ttf', 16)

    screen.blit((font.render(globalFeedback, True, teal)), (25, 380))
    hits = "Hits: " + str(goodHits)
    misses = "Misses: " + str(badHits)
    screen.blit((font.render(hits, True, teal)), (25, 425))
    screen.blit((font.render(misses, True, teal)), (25, 450))

    game.show_colums(screen)
    
    font = pygame.font.Font('freesansbold.ttf', 24)

    for i in range(1, 8):
        screen.blit((font.render(str(i), True, teal)), ((i-1)*70+97, 110))

def startHit(index): # this function starts a 1234567 thing
    global checkNewBeat
    for i in range(7):
        time.sleep(hitOffset)

        if i < 7:
            if game.active:
                game.update_cursor(screen, i)
            else:
                return 
        
        if i < 6:
            game.beatEffect.play()
        else:
            game.hitEffect.play()
        time.sleep(LEVEL_HITS_TIMING[index]-hitOffset)

    #move cursor using i

def showFeedback(feedback):
    global globalFeedback 
    globalFeedback = feedback
    drawScreen()

def background(): # this function is always running in the background. this lets things happen while we .sleep() or input()
    global levelIndex, playerIndex, badHits, accuracyList, game
    while True:

        #pygame stuff
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and game.active:
                    handling_input()

                #if event.key == pygame.K_SPACE and game.active == False:
                #    game.restart()


        pygame.display.update()
        clock.tick(60)

        #other stuff
        #if the time passes by a timestamp then activate that hit
        if levelIndex < len(LEVEL_HITS):
            if LEVEL_HITS[levelIndex] < getRuntime():
                #print("\n\n\n\n\n\n\n\nnew hit")
                startHit(levelIndex)
                levelIndex = levelIndex + 1


        if playerIndex < len(LEVEL_ACTUAL_HITS) and playerIndex <= levelIndex:
            if LEVEL_ACTUAL_HITS[playerIndex] < getRuntime() + leniency * 4:
                game.missEffect.play()
                playerIndex += 1
                badHits += 1
           
        #time.sleep(secondsPerBeat)


        if getRuntime() > LEVEL_END:
            
            game.backgroundMusic.stop()

            game.active = False

            accuracy = goodHits/len(LEVEL_HITS)

            waitTime = 1.5

            time.sleep(waitTime)

            if accuracy == 1:
                rank = "S+"
                time.sleep(waitTime)
                flavorText = "samurai says: you are a lifesaver"
            elif accuracy > .9:
                rank = "A"
                time.sleep(waitTime)
                flavorText = "samurai says: you are maestro"
            elif accuracy > .8:
                rank = "B"
                time.sleep(waitTime)
                flavorText = "samurai says: you are satisfactory"
            elif accuracy > .7:
                rank = "C"
                time.sleep(waitTime)
                flavorText = "samurai says: try again please"
            elif accuracy > .6:
                rank = "D"
                time.sleep(waitTime)
                flavorText = "samurai says: this is terrible form of alternative medicine"
            else:
                rank = "F"
                time.sleep(waitTime)
                flavorText = "samurai says: are you awake?"

            game.show_background(screen)
            font = pygame.font.Font('freesansbold.ttf', 20)
            teal = (0, 244, 207)
            screen.blit((font.render(rank, True, teal)), (150, 125))
            screen.blit((font.render(flavorText, True, teal)), (150, 250))
            
            time.sleep(waitTime)
            print("Average accuracy: ", end="")
            time.sleep(waitTime)
            absAccuracyList = []
            for i in accuracyList:
                absAccuracyList.append(abs(i))
            print(str(round(sum(absAccuracyList)/len(absAccuracyList))) + "ms")

            exit("Game end")

        sys.stdout.flush()

def printOnHit(offset):
    hitOrMiss = ""
    if -leniency*1000 <= offset <= leniency*1000:
        hitOrMiss = "HIT!  "
        global accuracyList
        accuracyList.append(offset)
    else:
        hitOrMiss = "MISS! "
    if offset < 0:
        return hitOrMiss + "Early by " + str(-offset) + "ms."
    elif offset > 0:
        return hitOrMiss + "Late by " + str(offset) + "ms."
    else:
        return hitOrMiss + "Perfect!"

def handling_input(): # on player input
    global goodHits, badHits, playerIndex, levelIndex
    #check every allowed hit in the level
    foundHit = False

    if playerIndex < len(LEVEL_ACTUAL_HITS):
        currentLevelHit = LEVEL_ACTUAL_HITS[playerIndex]


        if playerIndex <= levelIndex:
            #if within a certain threshold, be nice and let them hit
            if currentLevelHit + leniency > getRuntime() and currentLevelHit - leniency < getRuntime():
                showFeedback(printOnHit(getOffset(currentLevelHit)))
                playerIndex += 1
                goodHits += 1
                foundHit = True
            #if too far away from the hit, count as a miss

        if currentLevelHit + leniency * 4 > getRuntime() and currentLevelHit - leniency * 4 < getRuntime():
            #checks if the player already missed this note by pressing early


            if foundHit:
                pass
            elif playerIndex <= levelIndex:
                game.missEffect.play()
                showFeedback(printOnHit(getOffset(currentLevelHit)))
                playerIndex += 1
                badHits += 1
                foundHit = True
            else:
                game.blipEffect.play()
                showFeedback(printOnHit(getOffset(currentLevelHit)))
           
        #if no hit then bleh
        if not foundHit:
            game.blipEffect.play()
            if playerIndex <= levelIndex:
                showFeedback("Try hitting it closer to the beat buddy")
            #badHits = badHits + 1

#setup the background (idk how this works but stackoverflow does)
t = threading.Thread(target=background)
t.daemon = True
t.start()

game.start()

#check on userinputs
while True:
    if game.active:
        drawScreen()
        game.show_cursor(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            #blipEffect.play()
            handling_input()  

    pygame.display.update()
    clock.tick(60)