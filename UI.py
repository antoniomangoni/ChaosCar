import pygame
import numpy as np

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

class UI:
    def __init__(self,game):
        self.font = pygame.font.SysFont('Courier', 48)
        self.game = game

        self.tipfont = pygame.font.SysFont('Courier', 56, True)
        self.tipcounter = 0
    def update(self):
        return

    def render(self,rendering):
        self.timeimg = self.font.render('TIME:'+str(self.game.seconds), True, RED)
        rendering.screen.blit(self.timeimg, (20, 20))

        self.scoreimg = self.font.render('SCORE:'+str(self.game.scores), True, RED)
        rendering.screen.blit(self.scoreimg, (550, 20))
        
        if not self.game.car.isonroad:
            if self.game.elapsedTime%200>100:
                self.tipimg = self.tipfont.render('!!!OFF ROAD!!!', True, RED)
                rendering.screen.blit(self.tipimg, (400 - self.tipimg.get_width() // 2, 500 - self.tipimg.get_height() // 2))
        else:
            if self.game.car.ispartiallyoffroad:
                if self.game.elapsedTime%200>100:
                    self.tipimg = self.tipfont.render('!!OFF ROAD!!', True, YELLOW)
                    rendering.screen.blit(self.tipimg, (400 - self.tipimg.get_width() // 2, 500 - self.tipimg.get_height() // 2))