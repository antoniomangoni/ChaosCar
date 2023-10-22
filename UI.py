import pygame
import numpy as np

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
WHITE = (225,225,225)

class UI:
    def __init__(self,game):

        self.font = pygame.font.Font('ka1.ttf', 40)
        self.game = game


        self.game_state = "start"

        self.tipfont = pygame.font.Font('ka1.ttf', 40)
        self.tipcounter = 0
        self.tipfont_1 = pygame.font.Font('ka1.ttf', 55)
        self.tipcounter = 0
        #self.tipfont_2 = pygame.font.SysFont('Courier', 80, True)
        self.tipfont_2 = pygame.font.Font('ka1.ttf',45)
        #self.tipfont_2.set_italic(True)
        self.tipfont_3 = pygame.font.Font('ka1.ttf', 30)
        #self.tipfont_3.set_italic(True)
        self.control_btn_images = {}
        self.control_images = {}
        control_image_size = 80

        self.forwardbtn_image = pygame.image.load('Pixel_Art/forward_btn.png')
        self.forwardbtn_image = pygame.transform.scale(self.forwardbtn_image, (control_image_size, control_image_size))
        self.control_btn_images[pygame.K_w] = self.forwardbtn_image

        self.backwardbtn_image = pygame.image.load('Pixel_Art/backward_btn.png')
        self.backwardbtn_image = pygame.transform.scale(self.backwardbtn_image, (control_image_size, control_image_size))
        self.control_btn_images[pygame.K_SPACE] = self.backwardbtn_image

        self.rightbtn_image = pygame.image.load('Pixel_Art/right_btn.png')
        self.rightbtn_image = pygame.transform.scale(self.rightbtn_image, (control_image_size, control_image_size))
        self.control_btn_images[pygame.K_d] = self.rightbtn_image

        self.leftbtn_image = pygame.image.load('Pixel_Art/left_btn.png')
        self.leftbtn_image = pygame.transform.scale(self.leftbtn_image, (control_image_size, control_image_size))
        self.control_btn_images[pygame.K_a] = self.leftbtn_image
        
        #arrow!
        self.forward_image = pygame.image.load('Pixel_Art/forward.png')
        self.forward_image = pygame.transform.scale(self.forward_image, (control_image_size, control_image_size))
        self.control_images["accelerator"]=self.forward_image

        self.backward_image = pygame.image.load('Pixel_Art/backward.png')
        self.backward_image = pygame.transform.scale(self.backward_image, (control_image_size, control_image_size))
        self.control_images["brake_drift"]=self.backward_image

        self.right_image = pygame.image.load('Pixel_Art/right.png')
        self.right_image = pygame.transform.scale(self.right_image, (control_image_size, control_image_size))
        self.control_images["steerer_right"]=self.right_image

        self.left_image = pygame.image.load('Pixel_Art/left.png')
        self.left_image = pygame.transform.scale(self.left_image, (control_image_size, control_image_size))
        self.control_images["steerer_left"]=self.left_image

        self.btnbackground_image = pygame.image.load('Pixel_Art/btnbackground.png')

        self.HPBar_image = pygame.image.load('Pixel_Art/HPBar.png')
        self.HPBar_image = pygame.transform.scale(self.HPBar_image, (320, 64))
        self.HP_image = pygame.image.load('Pixel_Art/HP.png')
        self.HP_image = pygame.transform.scale(self.HP_image, (64, 64))

        self.offroadwarning_image = pygame.image.load('Pixel_Art/offroadwarning_fullscreen.png')
        self.offroadwarning_image = pygame.transform.scale(self.offroadwarning_image, (800, 600))
        self.offroadwarning_image = self.offroadwarning_image.convert_alpha()
    def update(self):
        pass

    def render(self,rendering):

        if self.game_state=="end" : 
            self.game_end(rendering)
            return
        
        if self.game.car.isdamage:
            rendering.screen.blit(self.offroadwarning_image, (0, 0))


        self.timeimg = self.font.render('TIME', True, RED)
        rendering.screen.blit(self.timeimg, (20, 20))
        self.timeimg = self.font.render(str(self.game.seconds), True, RED)
        rendering.screen.blit(self.timeimg, (55, 60))

        self.scoreimg = self.font.render('SCORE', True, RED)
        rendering.screen.blit(self.scoreimg, (580, 20))
        self.scoreimg = self.font.render(str(int(self.game.scores)), True, RED)
        rendering.screen.blit(self.scoreimg, (645, 60))

        # Show does car on the roaad
        if not self.game.car.isonroad:
            if self.game.elapsedTime%200 > 100:
                self.tipimg = self.tipfont_1.render('!!!OFF ROAD!!!', True, RED)
                rendering.screen.blit(self.tipimg, (400 - self.tipimg.get_width() // 2, 490 - self.tipimg.get_height() // 2))
        else:
            if self.game.car.ispartiallyoffroad:
                if self.game.elapsedTime%200 > 100:
                    self.tipimg = self.tipfont.render('!OFF ROAD!', True, YELLOW)
                    rendering.screen.blit(self.tipimg, (400 - self.tipimg.get_width() // 2, 490 - self.tipimg.get_height() // 2))
        # show background
        rendering.screen.blit(self.btnbackground_image, (0, 517))

        # show button
        if (self.game.willswaprole and self.game.elapsedTime%200 > 100) or not self.game.willswaprole:
            idx=0
            down_btn_idxs=[False,False,False,False]
            for key in self.control_btn_images:
                offset = 0
                if self.game.keys[key]==True:
                    offset = 10
                down_btn_idxs[idx]=True
                rendering.screen.blit(self.control_btn_images[key], (150+500/4*idx+32, 515+offset))
                idx+=1

            for i in range(4):
                role_name = self.game.car.roles[i]["name"]
                control_image = self.control_images[role_name]

                offset = 0
                if down_btn_idxs[i]:
                    offset = 10

                rendering.screen.blit(control_image, (150+500/4*i+32, 515+offset))

        
        rendering.screen.blit(self.HPBar_image, (220, 20))
        HPpercent = self.game.car.HP/100.0
        if self.game.car.HP>=0:
            for i in range(5):
                if HPpercent>=i*0.25:
                    rendering.screen.blit(self.HP_image, (220+i*64, 20))
                else:
                    if self.game.car.isdamage:
                        if self.game.elapsedTime%200 > 100:
                            rendering.screen.blit(self.HP_image, (220+i*64, 20))
                    else:
                        rendering.screen.blit(self.HP_image, (220+i*64, 20))
                    break

    def game_end(self,rendering):
        self.timeimg = self.tipfont_1.render('GAME OVER!', True, RED)
        rendering.screen.blit(self.timeimg, (150, 200))

        self.timeimg = self.tipfont_2.render('TIME: '+str(self.game.seconds), True, RED)
        rendering.screen.blit(self.timeimg, (150, 270))

        self.timeimg = self.tipfont_2.render('SCORE: '+str(self.game.scores), True, RED)
        rendering.screen.blit(self.timeimg, (150, 340))

        if self.game.elapsedTime%200 > 100:
            self.tipimg = self.tipfont.render('PRESS WHITE BUTTON', True, WHITE)
            self.screen.blit(self.tipimg, (400 - self.tipimg.get_width() // 2, 490 - self.tipimg.get_height() // 2))
            self.tipimg = self.tipfont.render('TO RESTART!', True, WHITE)
            self.screen.blit(self.tipimg, (400 - self.tipimg.get_width() // 2, 535 - self.tipimg.get_height() // 2))

    def change_ui_state(self, state="start"):
        self.game_state = state
