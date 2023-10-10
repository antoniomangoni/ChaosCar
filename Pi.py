import RPi.GPIO as GPIO  
import pygame
class PI:
    def __init__(self,game):
        self.game = game
        GPIO.setmode(GPIO.BOARD)
        self.KEY_W = 31
        self.KEY_A = 33
        self.KEY_S = 35
        self.KEY_D = 37
        GPIO.setup(self.KEY_W,GPIO.IN,GPIO.PUD_UP)
        GPIO.setup(self.KEY_A,GPIO.IN,GPIO.PUD_UP)
        GPIO.setup(self.KEY_S,GPIO.IN,GPIO.PUD_UP)
        GPIO.setup(self.KEY_D,GPIO.IN,GPIO.PUD_UP)
        self.keys={}

    def read_input(self):
        self.keys[pygame.K_w] = False
        self.keys[pygame.K_SPACE] = False
        self.keys[pygame.K_a] = False
        self.keys[pygame.K_d] = False

        if GPIO.input(self.KEY_W) == 0:
            self.keys[pygame.K_w] = True
        if GPIO.input(self.KEY_S) == 0:
            self.keys[pygame.K_SPACE] = True
        if GPIO.input(self.KEY_A) == 0:
            self.keys[pygame.K_a] = True
        if GPIO.input(self.KEY_D) == 0:
            self.keys[pygame.K_d] = True
        return self.keys