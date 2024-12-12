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

game = Game('img/column2.png', 'img/cursor.jpg', 'img/background2.jpg')
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


LEVEL_ACTUAL_HITS = [] # timing of when they actually have to hit


leniency = .1 #if hit is within this many seconds (+-) of a valid input then allow it
hitOffset = 0 #offset for hit after beat
beatOffset = -0.03 #offset for beat in relation to music
#secondsPerBeat = .5 #how many seconds are in each "beat" of the song. replaced with levelhitstiming
goodHits = 0 #how many times player got a good hit
badHits = 0 #how many times player missed a note
levelIndex = 0 #what hit the program is on
playerIndex = 0 #what hit the player is on (this should always be lower than or equal to levelindex)
accuracyList = [] #list of offsets


start = time.time() # set up the time at the start


for i in range(len(LEVEL_HITS)):
    LEVEL_ACTUAL_HITS.append(LEVEL_HITS[i] + LEVEL_HITS_TIMING[i]*6 + beatOffset)


game.backgroundMusic.play()
        
game.show_background(screen)
game.show_colums(screen)


#set up graphics
print("\nenter on the 7th beat")
sys.stdout.write("\033[K")
print("\n\n\n\n\n")
for i in range(5):
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")

def getRuntime(): # this function returns how much time since the program started (useful for getting time on the level)
    return time.time() - start

def getOffset(time): #this function returns how off you were in ms
    return int((getRuntime() - time - hitOffset)*1000)

def startHit(index): # this function starts a 1234567 thing
    
    for i in range(7):
        sys.stdout.write(f"""
  {"     "*i}{i+1}
{7*"  |  "}
              """)
        sys.stdout.write("\033[3F")
        sys.stdout.flush()
        time.sleep(hitOffset)
        if i < 6:
            game.beatEffect.play()
        else:
            game.hitEffect.play()


        if i < 7:
            time.sleep(LEVEL_HITS_TIMING[index]-hitOffset)
        if game.active:
            game.show_background(screen)
            game.show_colums(screen)
            teal = (0, 244, 207)
            font = pygame.font.Font('freesansbold.ttf', 16)
            for i in range(1, 8):
                screen.blit((font.render(str(i), True, teal)), ((i-1)*70+90, 120))
            game.update_cursor(screen, i+1)

    
    game.show_cursor(screen)
    #move cursor using i

def updateScore():
    #print score
    print("\n\n\n\n")
    print("Hits: " + str(goodHits))
    print("Misses: " + str(badHits))
    sys.stdout.write("\033[7F")



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

                if event.key == pygame.K_SPACE and game.active == False:
                    game.restart()


        pygame.display.update()
        clock.tick(60)


        #other stuff

        #sys.stdout.write("\033[K") #this line clears all i think
        #print(x, end='\r')
        #if the time passes by a timestamp then activate that hit
        if levelIndex < len(LEVEL_HITS):
            if LEVEL_HITS[levelIndex] < getRuntime():
                #print("\n\n\n\n\n\n\n\nnew hit")
                startHit(levelIndex)
                levelIndex = levelIndex + 1


        if playerIndex < len(LEVEL_ACTUAL_HITS) and playerIndex <= levelIndex:
            if LEVEL_ACTUAL_HITS[playerIndex] < getRuntime() + leniency * 4:
                #sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
                print("    Missed beat", end="\r")
                game.missEffect.play()
                playerIndex += 1
                badHits += 1
                updateScore()
           
        #time.sleep(secondsPerBeat)


        if getRuntime() > LEVEL_END:

            accuracy = goodHits/len(LEVEL_HITS)

            print("\n\n\n\n")
            for i in range(5):
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
            print("Your rank:")

            waitTime = 1.5

            time.sleep(waitTime)

            if accuracy == 1:
                print("S+")
                time.sleep(waitTime)
                print("samurai says: you are a lifesaver")
            elif accuracy > .9:
                print("A")
                time.sleep(waitTime)
                print("samurai says: you are maestro")
            elif accuracy > .8:
                print("B")
                time.sleep(waitTime)
                print("samurai says: you are satisfactory")
            elif accuracy > .7:
                print("C")
                time.sleep(waitTime)
                print("samurai says: try again please")
            elif accuracy > .6:
                print("D")
                time.sleep(waitTime)
                print("samurai says: this is terrible form of alternative medicine")
            else:
                print("F")
                time.sleep(waitTime)
                print("samurai says: are you awake")
               
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
        hitOrMiss = "   HIT!  "
        global accuracyList
        accuracyList.append(offset)
    else:
        hitOrMiss = "   MISS! "
    if offset < 0:
        return hitOrMiss + "Early by " + str(-offset) + "ms."
    elif offset > 0:
        return hitOrMiss + " Late by " + str(offset) + "ms."
    else:
        return hitOrMiss + "Perfect!"

def handling_input(): # on player input
    global goodHits, badHits, playerIndex, levelIndex
    #check every allowed hit in the level
    foundHit = False


#SOMETHING HERE TODO HELP AHHHHHHH REPLACE ALL i WITH TIHS VAR DOESNT WORK


    if playerIndex < len(LEVEL_ACTUAL_HITS):
        currentLevelHit = LEVEL_ACTUAL_HITS[playerIndex]


        if playerIndex <= levelIndex:
            #if within a certain threshold, be nice and let them hit
            if currentLevelHit + leniency > getRuntime() and currentLevelHit - leniency < getRuntime():
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
                print(printOnHit(getOffset(currentLevelHit)), end="\r")
                playerIndex += 1
                goodHits += 1
                foundHit = True
            #if too far away from the hit, count as a miss
        if currentLevelHit + leniency * 4 > getRuntime() and currentLevelHit - leniency * 4 < getRuntime():
            #checks if the player already missed this note by pressing early


            if foundHit:
                print("", end="\r")
            elif playerIndex <= levelIndex:
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
                game.missEffect.play()
                print(printOnHit(getOffset(currentLevelHit)), end="\r")
                playerIndex += 1
                badHits += 1
                foundHit = True
            else:
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
                game.blipEffect.play()
                print(printOnHit(getOffset(currentLevelHit)), end="\r")
           
        #if no hit then bleh
        if not foundHit:
            sys.stdout.write("\033[F")
            game.blipEffect.play()
            print("    not even close buddy     ", end="\r")
            #badHits = badHits + 1
    updateScore()

#setup the background (idk how this works but stackoverflow does)
t = threading.Thread(target=background)
t.daemon = True
t.start()


updateScore()
#check on userinputs
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            #blipEffect.play()
            handling_input()  

    pygame.display.update()
    clock.tick(60)

    #input stuff
    #inp = input()
    #handling_input()
    #if inp == 'q':
     #   sys.stdout.write("\033[K")
      #  print('quitting')
       # backgroundMusic.stop()
        #sys.exit()