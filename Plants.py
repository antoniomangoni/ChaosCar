import pygame
import numpy as np
import random
from shapely.geometry import Point, Polygon


from Spritesheet import SpriteSheet

class Plants:
    def __init__(self, screen_width, screen_height, road, render ):
        filename = 'Pixel_Art/Cactus.png'
        piece_ss = SpriteSheet(filename)
        s =64
        half = [screen_width/2,screen_height/2]
        self.rect =[np.int16(road.road_min_x-half[0]),
                    np.int16(road.road_max_x+half[0]),
                    np.int16(road.road_min_y-half[1]),
                    np.int16(road.road_max_y+half[1])] 
        self.image = []
        for i in range(2):
            for j in range(11):
                self.image.append(piece_ss.image_at((j*s,i*s,s,s),(0,0,0,0)))
        self.surface = pygame.Surface((self.rect[1]-self.rect[0],self.rect[3]-self.rect[2]),pygame.SRCALPHA)
        road_polygon = Polygon(render.road_polygon_points)
        x = 0
        y = 0
        while(y<self.rect[3]-self.rect[2]):
            while(x<self.rect[1]-self.rect[0]):
                tx = x+random.randint(0,80)
                ty = y+random.randint(0,80)
                image = self.image[random.randint(0,21)]
                poly = self.construct_bb([tx+self.rect[0],ty+self.rect[2]])
                if(not poly.intersection(road_polygon)):
                    self.surface.blit(image,(tx,ty))
                x+=150
            y+=150
            x = self.rect[0]
    
    def construct_bb(self,pos):
        left =np.array(pos)
        right = np.array(pos)+np.array([pos[0]+64,pos[1]])
        bleft = np.array(pos) + np.array([pos[0],pos[1]+64])
        bright = np.array(pos) + np.array([pos[0]+64,pos[1]+64])
        return Polygon([left,bleft,bright,right])

    def draw(self,screen,render):
        offsetx = render.pos[0]-render.offset[0]
        offsety = render.pos[1] -render.offset[1]
        screen.blit(self.surface,(self.rect[0]-offsetx,self.rect[2]-offsety))
