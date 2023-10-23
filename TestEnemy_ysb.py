import pygame
import numpy as np
import random

class Enemystate():
    idle = 0
    Chase  = 1
    Attack = 2



class TestEnemy:
    def __init__(self, game, pos):
        self.game = game
        self.pos = pos
        self.sprite = pygame.image.load('Pixel_Art/sandstorm.png')
        self.sprite = pygame.transform.scale(self.sprite,(2560,1000))
        self.sprite = self.sprite.convert_alpha()
        self.itimer = 0.0
        self.car = game.car
        self.isinsandstorm = False
    def spawn(self):       
        pass

    def draw(self,screen,render):
        offsetx = render.pos[0]-render.offset[0]
        offsety = render.pos[1]-render.offset[1]
        screen.blit(self.sprite,(self.pos[0]-offsetx,self.pos[1]-offsety))

    def update(self,dt):
        self.pos[1]-=dt*0.02
        distance = self.car.position[1] - self.pos[1]

        if distance>100:
            self.car.HP-=0.2
            self.car.isdamage = True
            self.isinsandstorm = True
        else:
            self.isinsandstorm = False
        pass

    def chase(self):
        pass
