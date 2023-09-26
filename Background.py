import pygame
import numpy as np

class Background:
    def __init__(self, screen_width, screen_height):
        self.screenWidth = screen_width
        self.screenHeight = screen_height
        self.height = 420
        self.width = 630
        self.image = pygame.image.load('Pixel_Art/sand.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(0,0))
        

    def draw(self,screen, render):
        offsetx = render.pos[0]-render.offset[0]
        offsety = render.pos[1] -render.offset[1]
        ox = np.int32(offsetx/self.width)*self.width-self.width
        oy = np.int32(offsety/self.height)*self.height- self.height
        x =ox
        y =oy
        while(y<self.screenHeight+render.pos[1]+render.offset[1]):
            while(x<self.screenWidth+render.pos[0]+render.offset[0]):
                screen.blit(self.image,(x-render.pos[0]+render.offset[0],y-render.pos[1]+render.offset[1]))
                x+=self.width
            x = ox
            y+=self.height
       

       