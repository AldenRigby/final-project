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

start = time.time() # set up the time at the start
#set up graphics
print("enter on the 7th beat")
print("\n\n\n\n")
sys.stdout.write("\033[5F")

def getRuntime(): # this function returns how much time since the program started (useful for getting time on the level)
    return time.time() - start

def startHit(index): # this function starts a 1234567 thing
    for i in range(7):
        print(f"""\n{i*"  |  "}{i+1}
              
              """)
        sys.stdout.write("\033[4F")
        sys.stdout.flush()
        sound1.play()
        time.sleep(LEVEL_HITS_TIMING[index])


def background(): # this function is always running in the backgroud. this lets things happen while we .sleep()
    x = 0
    levelIndex = 0 #what hit the program is on
    while True:
        x += 1

        sys.stdout.write("\033[K")
        #print(x, end='\r')
        if levelIndex < len(LEVEL_HITS):
            if LEVEL_HITS[levelIndex] < getRuntime():
                #print("\n\n\n\n\n\n\n\nnew hit")
                startHit(levelIndex)
                levelIndex = levelIndex + 1
            
        #time.sleep(secondsPerBeat)

        sys.stdout.flush()



def handling_input(inp): # on player input
    #print('Got {}'.format(inp), end="\r")
    #print(getRuntime(), end="\r")
    #sound1.play()

    #check every allowed hit in the level
    foundHit = False
    for i in LEVEL_ACTUAL_HITS:
        #if within a certain threshold, be nice and let them hit
        if i + leniency > getRuntime() and i - leniency < getRuntime():
            sys.stdout.write("\033[F")
            print("    good job you hit      ", end="\r")
            foundHit = True
            break

    if not foundHit:
        sys.stdout.write("\033[F")
        print("    bruh you didn't hit     ", end="\r")

#setup the background (idk how this works but stackoverflow does)
t = threading.Thread(target=background)
t.daemon = True
t.start()

#check on userinputs
while True:
    inp = input()
    handling_input(inp)
    if inp == 'q':
        sys.stdout.write("\033[K")
        print('quitting')
        sys.exit()