import time
import threading
import sys
import pygame

pygame.mixer.init()
sound1 = pygame.mixer.Sound('button.mp3')  # Load a sound.
#backgroundMusic = pygame.mixer.Sound('XXX.mp3')  # Load a sound.
#hitEffect = pygame.mixer.Sound('XXX.mp3')  # Load a sound.
#missEffect = pygame.mixer.Sound('XXX.mp3')  # Load a sound.

LEVEL_HITS = [2, 3] #how many seconds after program runs to get a hit.
leniency = .2 #if hit is within this many seconds of a valid input then allow it
secondsPerBeat = .5

start = time.time()
print("enter on the 5th and 7th beat")
print("\n\n\n\n")
sys.stdout.write("\033[5F")

def getRuntime():
    return time.time() - start

def background():
    x = 0
    while True:
        x += 1

        sys.stdout.write("\033[K")
        #print(x, end='\r')
        print(f"""
{x*"  |  "}{x}
              
              """)

        sound1.play()
        time.sleep(secondsPerBeat)

        sys.stdout.write("\033[4F")
        sys.stdout.flush()

def handling_input(inp):
    #print('Got {}'.format(inp), end="\r")
    #print(getRuntime(), end="\r")
    sound1.play()

    foundHit = False
    for i in LEVEL_HITS:
        if i + leniency > getRuntime() and i - leniency < getRuntime():
            sys.stdout.write("\033[F")
            print("    good job you hit", end="\r")
            foundHit = True
            break

    if not foundHit:
        sys.stdout.write("\033[F")
        print("    bruh you didn't hit", end="\r")

t = threading.Thread(target=background)
t.daemon = True
t.start()

while True:
    inp = input()
    handling_input(inp)
    if inp == 'q':
        sys.stdout.write("\033[K")
        print('quitting')
        sys.exit()