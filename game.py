import pygame

class Game:
    def __init__(self, column_img, cursor_img, background_img):
        self.column1 = pygame.image.load(column_img).convert_alpha()
        self.column2 = pygame.image.load(column_img).convert_alpha()
        self.column3 = pygame.image.load(column_img).convert_alpha()
        self.column4 = pygame.image.load(column_img).convert_alpha()
        self.column5 = pygame.image.load(column_img).convert_alpha()
        self.column6 = pygame.image.load(column_img).convert_alpha()
        self.column7 = pygame.image.load(column_img).convert_alpha()
        self.columns = []
        self.columns.append(self.column1, self.column2, self.column3, self.column4, self.column5, self.column6, self.column7)

        self.cursor = pygame.image.load(cursor_img).convert_alpha()
       # self.cursor_rect = self.cursor.get_rect(center = (, ))
        self.background = pygame.image.load(background_img).convert_alpha()

    def resize_imgs(self):
        for column in self.columns:
            column = pygame.transform.scale(column, (10, 20)) #probably have to change later

        self.cursor = pygame.transform.scale(self.cursor, (11, 21))
        self.background = pygame.transform.scale(self.background, (600, 500))

    def show_background(self, screen):
        screen.blit(self.background, (0, 0))

    def show_colums(self, screen):
        for i in range(len(self.columns)):
            screen.blit(self.columns[i], (i*70+55, 140))