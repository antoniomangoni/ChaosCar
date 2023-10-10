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

        self.control_images = {}
        control_image_size = 80

        self.forwardbtn_image = pygame.image.load('Pixel_Art/forwardbtn.png')
        self.forwardbtn_image = pygame.transform.scale(self.forwardbtn_image, (control_image_size, control_image_size))
        self.control_images["accelerator"]=self.forwardbtn_image

        self.backwardbtn_image = pygame.image.load('Pixel_Art/backwardbtn.png')
        self.backwardbtn_image = pygame.transform.scale(self.backwardbtn_image, (control_image_size, control_image_size))
        self.control_images["brake_drift"]=self.backwardbtn_image

        self.rightbtn_image = pygame.image.load('Pixel_Art/rightbtn.png')
        self.rightbtn_image = pygame.transform.scale(self.rightbtn_image, (control_image_size, control_image_size))
        self.control_images["steerer_right"]=self.rightbtn_image

        self.leftbtn_image = pygame.image.load('Pixel_Art/leftbtn.png')
        self.leftbtn_image = pygame.transform.scale(self.leftbtn_image, (control_image_size, control_image_size))
        self.control_images["steerer_left"]=self.leftbtn_image

        self.btnbackground_image = pygame.image.load('Pixel_Art/btnbackground.png')

    def update(self):
        return

    def render(self,rendering):
        self.timeimg = self.font.render('TIME:'+str(self.game.seconds), True, RED)
        rendering.screen.blit(self.timeimg, (20, 20))

        self.scoreimg = self.font.render('SCORE:'+str(self.game.scores), True, RED)
        rendering.screen.blit(self.scoreimg, (550, 20))
        
        if not self.game.car.isonroad:
            if self.game.elapsedTime%200 > 100:
                self.tipimg = self.tipfont.render('!!!OFF ROAD!!!', True, RED)
                rendering.screen.blit(self.tipimg, (400 - self.tipimg.get_width() // 2, 500 - self.tipimg.get_height() // 2))
        else:
            if self.game.car.ispartiallyoffroad:
                if self.game.elapsedTime%200 > 100:
                    self.tipimg = self.tipfont.render('!!OFF ROAD!!', True, YELLOW)
                    rendering.screen.blit(self.tipimg, (400 - self.tipimg.get_width() // 2, 500 - self.tipimg.get_height() // 2))

        rendering.screen.blit(self.btnbackground_image, (0, 500))

        for i in range(len(self.game.car.roles)):
            role_name = self.game.car.roles[i]["name"]
            control_image = self.control_images[role_name]

            offset = 0
            if self.game.btn_status_dict[role_name]==True:
                offset = 10

            rendering.screen.blit(control_image, (150+500/4*i+32, 510+offset))
        
        

