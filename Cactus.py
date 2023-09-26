import pygame

class Cactus:
    def __init__(self):
        self.image = pygame.image.load('Pixel_Art/sand.png')
        self.rect = self.image.get_rect(topleft=(0,0))
        

    def draw(self,screen,pos):
       screen.blit(self.image,pos)
       