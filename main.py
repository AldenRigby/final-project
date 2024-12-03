#something like this:
#https://rhythmdr.com/cny/

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
goodHits = 0 #rework how hits and stuff work because right now it's really bad
badHits = 0

start = time.time() # set up the time at the start
#set up graphics
print("\nenter on the 7th beat\n")
print("\n\n\n\n")
sys.stdout.write("\033[5F")

def getRuntime(): # this function returns how much time since the program started (useful for getting time on the level)
    return time.time() - start

def startHit(index): # this function starts a 1234567 thing
    for i in range(7):
        print(f"""
  {"     "*i}{i+1}
{7*"  |  "}
              """)
        sys.stdout.write("\033[4F")
        sys.stdout.flush()
        sound1.play()
        time.sleep(LEVEL_HITS_TIMING[index])


def background(): # this function is always running in the backgroud. this lets things happen while we .sleep() or input()
    levelIndex = 0 #what hit the program is on
    while True:
        #sys.stdout.write("\033[K") #this line clears all i think
        #print(x, end='\r')
        #if the time passes by a timestamp then activate that hit
        if levelIndex < len(LEVEL_HITS):
            if LEVEL_HITS[levelIndex] < getRuntime():
                #print("\n\n\n\n\n\n\n\nnew hit")
                startHit(levelIndex)
                levelIndex = levelIndex + 1
            
        #time.sleep(secondsPerBeat)

        sys.stdout.flush()

def handling_input(inp): # on player input
    global goodHits, badHits
    #check every allowed hit in the level
    foundHit = False
    for i in LEVEL_ACTUAL_HITS:
        #if within a certain threshold, be nice and let them hit
        if i + leniency > getRuntime() and i - leniency < getRuntime():
            sys.stdout.write("\033[F")
            print("    good job you hit      ", end="\r")
            goodHits = goodHits + 1
            foundHit = True
            break
    #if no hit then bleh
    if not foundHit:
        sys.stdout.write("\033[F")
        print("    bruh you didn't hit     ", end="\r")
        badHits = badHits + 1

#setup the background (idk how this works but stackoverflow does)
t = threading.Thread(target=background)
t.daemon = True
t.start()

#check on userinputs
while True:
    #print score
    print("\n\n\n\n")
    print("Hits: " + str(goodHits))
    print("Misses: " + str(badHits))
    sys.stdout.write("\033[7F")

    #input stuff
    inp = input()
    handling_input(inp)
    if inp == 'q':
        sys.stdout.write("\033[K")
        print('quitting')
        sys.exit()