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
sound1 = pygame.mixer.Sound('button.mp3')  # Load a sound.
#backgroundMusic = pygame.mixer.Sound('XXX.mp3')  # Load a sound.
#hitEffect = pygame.mixer.Sound('XXX.mp3')  # Load a sound.
#missEffect = pygame.mixer.Sound('XXX.mp3')  # Load a sound.

#how many seconds after program runs to start a 7 thing. //
#how many seconds between beats for the 7 hit above thingy
LEVEL_HITS        = [0,  4,   6] 
LEVEL_HITS_TIMING = [.5, .25, .5]
LEVEL_ACTUAL_HITS = [] # timing of when they actually have to hit
for i in range(len(LEVEL_HITS)):
    LEVEL_ACTUAL_HITS.append(LEVEL_HITS[i] + LEVEL_HITS_TIMING[i]*6)

leniency = .2 #if hit is within this many seconds (+-) of a valid input then allow it
secondsPerBeat = .5 #how many seconds are in each "beat" of the song.
goodHits = 0 #how many times player got a good hit
badHits = 0 #how many times player missed a note
levelIndex = 0 #what hit the program is on
playerIndex = 0 #what hit the player is on (this should always be lower than or equal to levelindex)

start = time.time() # set up the time at the start

#set up graphics
print("\nenter on the 7th beat\n")
print("\n\n\n\n")
sys.stdout.write("\033[5F")

def getRuntime(): # this function returns how much time since the program started (useful for getting time on the level)
    return time.time() - start

def startHit(index): # this function starts a 1234567 thing
    for i in range(7):
        sys.stdout.write(f"""
  {"     "*i}{i+1}
{7*"  |  "}
              """)
        sys.stdout.write("\033[3F")
        sys.stdout.flush()
        sound1.play()
        time.sleep(LEVEL_HITS_TIMING[index])

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
            if LEVEL_ACTUAL_HITS[playerIndex] < getRuntime() + leniency * 2:
                #sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
                print("    missed ....", end="\r")
                playerIndex += 1
                badHits += 1
                updateScore()
            
        #time.sleep(secondsPerBeat)

        sys.stdout.flush()

def handling_input(inp): # on player input
    global goodHits, badHits, playerIndex, levelIndex
    #check every allowed hit in the level
    foundHit = False
    for i in LEVEL_ACTUAL_HITS:
        if playerIndex <= levelIndex:
            #if within a certain threshold, be nice and let them hit
            if i + leniency > getRuntime() and i - leniency < getRuntime():
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
                print("    good job you hit", end="\r")
                playerIndex += 1
                goodHits = goodHits + 1
                foundHit = True
                break
            #if too far away from the hit, count as a miss
        if i + leniency * 2 > getRuntime() and i - leniency * 2 < getRuntime():
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            #checks if the player already missed this note by pressing early
            if playerIndex > levelIndex:
                print("    already got that note", end="\r")
            else:
                print("    that was close", end="\r")
                playerIndex += 1
                badHits = badHits + 1
            foundHit = True
            break
    #if no hit then bleh
    if not foundHit:
        sys.stdout.write("\033[F")
        print("    not even close buddy     ", end="\r")
        #badHits = badHits + 1

#setup the background (idk how this works but stackoverflow does)
t = threading.Thread(target=background)
t.daemon = True
t.start()

#check on userinputs
while True:
    updateScore()
    #input stuff
    inp = input()
    handling_input(inp)
    if inp == 'q':
        sys.stdout.write("\033[K")
        print('quitting')
        sys.exit()