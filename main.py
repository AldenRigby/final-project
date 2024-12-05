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
beatEffect = pygame.mixer.Sound('sounds/kick.mp3')  # every beat this plays
backgroundMusic = pygame.mixer.Sound('sounds/Samurai Techno.mp3')  # music
blipEffect = pygame.mixer.Sound('sounds/blip.mp3')  # when player makes input not anywhere near the actual hit
hitEffect = pygame.mixer.Sound('sounds/hit.mp3')  # plays when player is supposed to hit
missEffect = pygame.mixer.Sound('sounds/miss.mp3')  # miss
#drumEffect = pygame.mixer.Sound('sounds/drum.mp3')  # if player hits right then this should play soon after

#how many seconds after program runs to start a 7 thing. //
#how many seconds between beats for the 7 hit above thingy
#samurai techno is 200 bpm. .6 for fast, .3 for medium, .15 for fast
LEVEL_HITS        = [0,  4.8,9.6,14.4,16.8]
LEVEL_HITS_TIMING = [.6, .6, .6, .15, .15]
LEVEL_ACTUAL_HITS = [] # timing of when they actually have to hit
for i in range(len(LEVEL_HITS)):
    LEVEL_ACTUAL_HITS.append(LEVEL_HITS[i] + LEVEL_HITS_TIMING[i]*6)

leniency = .1 #if hit is within this many seconds (+-) of a valid input then allow it
secondsPerBeat = .5 #how many seconds are in each "beat" of the song.
goodHits = 0 #how many times player got a good hit
badHits = 0 #how many times player missed a note
levelIndex = 0 #what hit the program is on
playerIndex = 0 #what hit the player is on (this should always be lower than or equal to levelindex)

start = time.time() # set up the time at the start
backgroundMusic.play()

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
        if i < 6:
            beatEffect.play()
        else:
            hitEffect.play()
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
                missEffect.play()
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
        if i + leniency * 3 > getRuntime() and i - leniency * 3 < getRuntime():
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            #checks if the player already missed this note by pressing early
            if playerIndex > levelIndex:
                blipEffect.play()
                print("    already got that note", end="\r")
            else:
                missEffect.play()
                print("    that was close", end="\r")
                playerIndex += 1
                badHits = badHits + 1
            foundHit = True
            break
    #if no hit then bleh
    if not foundHit:
        sys.stdout.write("\033[F")
        blipEffect.play()
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
        backgroundMusic.stop()
        sys.exit()
