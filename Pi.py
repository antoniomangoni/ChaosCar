import RPi.GPIO as GPIO  
import pygame
class PI:
    def __init__(self,game):
        self.game = game
        GPIO.setmode(GPIO.BOARD)
        self.KEY_ENTER = 29
        self.KEY_W = 31
        self.KEY_A = 33
        self.KEY_S = 35
        self.KEY_D = 37
        GPIO.setup(self.KEY_ENTER,GPIO.IN,GPIO.PUD_UP)
        GPIO.setup(self.KEY_W,GPIO.IN,GPIO.PUD_UP)
        GPIO.setup(self.KEY_A,GPIO.IN,GPIO.PUD_UP)
        GPIO.setup(self.KEY_S,GPIO.IN,GPIO.PUD_UP)
        GPIO.setup(self.KEY_D,GPIO.IN,GPIO.PUD_UP)

        self.VIB_W = 32
        self.VIB_A = 36
        self.VIB_S = 38
        self.VIB_D = 40
        GPIO.setup(self.VIB_W, GPIO.OUT)
        GPIO.output(self.VIB_W, GPIO.LOW)
        GPIO.setup(self.VIB_A, GPIO.OUT)
        GPIO.output(self.VIB_A, GPIO.LOW)
        GPIO.setup(self.VIB_S, GPIO.OUT)
        GPIO.output(self.VIB_S, GPIO.LOW)
        GPIO.setup(self.VIB_D, GPIO.OUT)
        GPIO.output(self.VIB_D, GPIO.LOW)
        self.keys={}

    def read_input(self):
        self.keys[pygame.K_w] = False
        self.keys[pygame.K_SPACE] = False
        self.keys[pygame.K_a] = False
        self.keys[pygame.K_d] = False
        self.keys[pygame.K_KP_ENTER] = False
        if GPIO.input(self.KEY_ENTER) == 0:
            self.keys[pygame.K_KP_ENTER] = True
        if GPIO.input(self.KEY_W) == 0:
            self.keys[pygame.K_w] = True
        if GPIO.input(self.KEY_S) == 0:
            self.keys[pygame.K_SPACE] = True
        if GPIO.input(self.KEY_A) == 0:
            self.keys[pygame.K_a] = True
        if GPIO.input(self.KEY_D) == 0:
            self.keys[pygame.K_d] = True
        return self.keys
    
    def vibrate(self):
        GPIO.output(self.VIB_W, GPIO.HIGH)
        GPIO.output(self.VIB_A, GPIO.HIGH)
        GPIO.output(self.VIB_S, GPIO.HIGH)
        GPIO.output(self.VIB_D, GPIO.HIGH)
    def stopvibrate(self):
        GPIO.output(self.VIB_W, GPIO.LOW)
        GPIO.output(self.VIB_A, GPIO.LOW)
        GPIO.output(self.VIB_S, GPIO.LOW)
        GPIO.output(self.VIB_D, GPIO.LOW)