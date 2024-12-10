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

pygame.mixer.init() # setup pygame mixer
beatEffect = pygame.mixer.Sound('./sounds/kick.mp3')  # every beat this plays
backgroundMusic = pygame.mixer.Sound('./sounds/Samurai Techno.mp3')  # music
blipEffect = pygame.mixer.Sound('./sounds/blip.mp3')  # when player makes input not anywhere near the actual hit
hitEffect = pygame.mixer.Sound('./sounds/hit.mp3')  # plays when player is supposed to hit
missEffect = pygame.mixer.Sound('./sounds/miss.mp3')  # miss
#drumEffect = pygame.mixer.Sound('./sounds/drum.mp3')  # if player hits right then this should play soon after


#how many seconds after program runs to start a 7 thing. //
#how many seconds between beats for the 7 hit above thingy
#samurai techno is 200 bpm. .6 for fast, .3 for medium, .15 for fast
LEVEL_BPM = 200
LEVEL_SECONDS_PER_BEAT = 60/LEVEL_BPM
#LEVEL_HITS_BEAT        = [0, 32, 48, 51.16, 59.16]
#LEVEL_HITS_TIMING_BEAT = [4, 2,  1, .5,    .5]
#                                                                                the drop V                                                                                                                                   #slowdown V
LEVEL_HITS        = [0,    9.6, 14.4, 16.55, 17.75, 19.25, 21.65, 24.05, 26.15, 27.35, 28.8, 30,  31.2, 32.4, 33.6, 34.8, 36,  37.2, 38.4, 39.6, 40.8, 42,  43.2, 44.4, 45.6, 46.8, 48,  49.2, 50.4, 51.6, 52.8, 54,  55.2, 56.4, 57.6, 58.95, 60,  61.35,  62.4,  63.75, 64.8, 65.85, 67.05, 68.05, 72.3]
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
gameRunning = True

start = time.time() # set up the time at the start

for i in range(len(LEVEL_HITS)):
    LEVEL_ACTUAL_HITS.append(LEVEL_HITS[i] + LEVEL_HITS_TIMING[i]*6 + beatOffset)

backgroundMusic.play()

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
    return str(int((getRuntime() - time - hitOffset)*1000)) + "ms"

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
            beatEffect.play()
        else:
            hitEffect.play()

        if i < 7:
            time.sleep(LEVEL_HITS_TIMING[index]-hitOffset)

    #move cursor using i

def updateScore():
    #print score
    print("\n\n\n\n")
    print("Hits: " + str(goodHits))
    print("Misses: " + str(badHits))
    sys.stdout.write("\033[7F")


def background(): # this function is always running in the backgroud. this lets things happen while we .sleep() or input()
    global levelIndex, playerIndex, badHits
    while True:
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
                print("    missed ...." + str(playerIndex) + str(levelIndex), end="\r")
                missEffect.play()
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
            time.sleep(1.5)

            if accuracy == 1:
                print("S+")
                time.sleep(1.5)
                print("samurai says: you are a lifesaver")
            elif accuracy > .9:
                print("A")
                time.sleep(1.5)
                print("samurai says: you are maestro")
            elif accuracy > .8:
                print("B")
                time.sleep(1.5)
                print("samurai says: you are satisfactory")
            elif accuracy > .7:
                print("C")
                time.sleep(1.5)
                print("samurai says: try again please")
            elif accuracy > .6:
                print("D")
                time.sleep(1.5)
                print("samurai says: this is terrible form of alternative medicine")
            else:
                print("F")
                time.sleep(1.5)
                print("samurai says: are you awake")

            quit()

        sys.stdout.flush()

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
                print(f"{getOffset(currentLevelHit)} good job you hit", end="\r")
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
                missEffect.play()
                print(f"{getOffset(currentLevelHit)} that was close" + str(playerIndex) + str(levelIndex), end="\r")
                playerIndex += 1
                badHits += 1
                foundHit = True
            else:
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
                blipEffect.play()
                print("    already got that note" + str(playerIndex) + str(levelIndex), end="\r")
            
        #if no hit then bleh
        if not foundHit:
            sys.stdout.write("\033[F")
            blipEffect.play()
            print("    not even close buddy     ", end="\r")
            #badHits = badHits + 1
    updateScore()

#setup the background (idk how this works but stackoverflow does)
t = threading.Thread(target=background)
t.daemon = True
t.start()

updateScore()
#check on userinputs
while gameRunning:
    #input stuff
    inp = input()
    handling_input()
    if inp == 'q':
        sys.stdout.write("\033[K")
        print('quitting')
        backgroundMusic.stop()
        sys.exit()
