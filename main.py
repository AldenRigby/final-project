import time
import threading
import sys
import pygame
pygame.mixer.init()
sound1 = pygame.mixer.Sound('button.mp3')  # Load a sound.

start = time.time()

def getRuntime():
    return time.time() - start

def background():
    while True:
        for x in range(10):
            sys.stdout.write('\r'+str(x))
            time.sleep(.2)
            sys.stdout.flush()

def handling_input(inp):
    print('Got {}'.format(inp))
    sound1.play()

t = threading.Thread(target=background)
t.daemon = True
t.start()

while True:
    print(getRuntime())
    inp = input()
    handling_input(inp)
    if inp == 'q':
        print('quitting')
        sys.exit()