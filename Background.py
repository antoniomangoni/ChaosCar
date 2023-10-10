import pygame
import numpy as np

class Background:
    def __init__(self, screen_width, screen_height):
        self.screenWidth = screen_width
        self.screenHeight = screen_height
        self.height = 150
        self.width = 150
        filepath = 'Pixel_Art/sandmap/'
        self.images = [pygame.image.load(filepath+'sand0.png'),
                       pygame.image.load(filepath+'sand1.png'),
                       pygame.image.load(filepath+'sand2.png'),
                       pygame.image.load(filepath+'sand3.png')]
        for i in range(4):
            self.images[i] = self.images[i].convert()
            self.images[i] = pygame.transform.scale(self.images[i], (self.height, self.width))
        self.w =np.int8(self.screenWidth/self.width)+2
        self.h =np.int8(self.screenHeight/self.height)+2
        self.surface = pygame.Surface((screen_width,screen_height))

    '''
    def update_surface(self,nx,ny):
        for i in range(self.h):
            onx = nx
            for j in range(self.w):
                num = abs(nx)%2
                num += abs(ny)%3
                image = self.images[num]
                self.surface.blit(image,(j*self.width,i*self.height))
                nx+=1
            nx = onx
            ny+=1

    def compair_border(self,screen):
        return self.rect[0]>screen[0] or self.rect[1]>screen[1] or self.rect[0]<screen[2] or self.rect[0]<screen[3]
    '''

    def draw(self,screen, render):
        offsetx = render.pos[0]-render.offset[0]
        offsety = render.pos[1] -render.offset[1]
        nx =np.int32(offsetx/self.width)-1
        ny =np.int32(offsety/self.height)-1
        x = nx*self.width
        y = ny*self.height

        for i in range(self.w):
            ox =x
            onx = nx
            for j in range(self.w):
                num = abs(nx)%2
                num += abs(ny)%3
                image = self.images[num]
                screen.blit(image,(x-offsetx,y-offsety))
                x+=self.width
                nx += 1
            x = ox
            nx=onx
            y+=self.height
            ny+=1
        

       