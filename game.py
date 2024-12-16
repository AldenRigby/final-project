import pygame
import time

class Game:
    def __init__(self, column_img, cursor_img, background_img):
        #setup all 7 columns
        self.startTime = 0
        self.columns = []
        for i in range(7):
            self.columns.append(pygame.image.load(column_img).convert_alpha())

        self.cursor = pygame.image.load(cursor_img).convert_alpha()
       # self.cursor_rect = self.cursor.get_rect(center = (, ))
        self.background = pygame.image.load(background_img).convert_alpha()
        self.active = True
        self.font = pygame.font.SysFont(None, 48)
        pygame.mixer.init() # setup pygame mixer
        self.beatEffect = pygame.mixer.Sound('./sounds/kick.mp3')  # every beat this plays
        self.backgroundMusic = pygame.mixer.Sound('./sounds/Samurai Techno.mp3')  # music
        self.blipEffect = pygame.mixer.Sound('./sounds/blip.mp3')  # when player makes input not anywhere near the actual hit
        self.hitEffect = pygame.mixer.Sound('./sounds/hit.mp3')  # plays when player is supposed to hit
        self.missEffect = pygame.mixer.Sound('./sounds/miss.mp3')  # miss

        self.cursorRect = self.cursor.get_rect(center = (212, 350))
        #drumEffect = pygame.mixer.Sound('./sounds/drum.mp3')  # if player hits right then this should play soon after

    def resize_images(self):
        for i in range(7):
            self.columns[i] = pygame.transform.rotozoom(self.columns[i], 90, 1)
            self.columns[i] = pygame.transform.scale(self.columns[i], (40, 200))

        self.cursor = pygame.transform.scale(self.cursor, (40, 40))
        self.background = pygame.transform.scale(self.background, (600, 500))

    def show_background(self, screen):
        screen.blit(self.background, (0,0))

    def show_colums(self, screen):
        for i in range(len(self.columns)):
            screen.blit(self.columns[i], (i*70+85, 140)) 

    def show_cursor(self, screen):
        screen.blit(self.cursor, self.cursorRect)

    def update_cursor(self, screen, i):
        #screen.blit(self.cursor, (i*70 + 84, 220))
        self.cursorRect.centerx = i*70 + 212

    def game_over(self, screen, color):
        self.show_score("game_over", screen, color)

    def start(self):
        self.backgroundMusic.stop()
        self.backgroundMusic.play()
        self.active = True
        self.startTime = time.time()

    def end(self):
        self.backgroundMusic.stop()