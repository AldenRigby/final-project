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
        """""
        self.columns.append(self.column1)
        self.columns.append(self.column2)
        self.columns.append(self.column3)
        self.columns.append(self.column4)
        self.columns.append(self.column5)
        self.columns.append(self.column6)
        self.columns.append(self.column7)
        """

        self.cursor = pygame.image.load(cursor_img).convert_alpha()
       # self.cursor_rect = self.cursor.get_rect(center = (, ))
        self.background = pygame.image.load(background_img).convert_alpha()
        self.active = True
        self.font = pygame.font.SysFont(None, 48)


    def resize_images(self):
        #for column in self.columns:
        self.column1 = pygame.transform.scale(self.column1, (20, 200)) #probably have to change later
        self.column2 = pygame.transform.scale(self.column2, (20, 200))
        self.column3 = pygame.transform.scale(self.column3, (20, 200))
        self.column4 = pygame.transform.scale(self.column4, (20, 200))
        self.column5 = pygame.transform.scale(self.column5, (20, 200))
        self.column6 = pygame.transform.scale(self.column6, (20, 200))
        self.column7 = pygame.transform.scale(self.column7, (20, 200))
        self.columns.append(self.column1)
        self.columns.append(self.column2)
        self.columns.append(self.column3)
        self.columns.append(self.column4)
        self.columns.append(self.column5)
        self.columns.append(self.column6)
        self.columns.append(self.column7)

        self.cursor = pygame.transform.scale(self.cursor, (20, 10))
        self.background = pygame.transform.scale(self.background, (600, 500))

    def show_background(self, screen):
        screen.blit(self.background, (0,0))

    def show_colums(self, screen):
        for i in range(len(self.columns)):
            screen.blit(self.columns[i], (i*70+85, 140)) 

    def show_cursor(self, screen):
        screen.blit(self.cursor, (85, 125))