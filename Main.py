# Main.py
import pygame
import numpy as np
from Car import Car
from Road import Road
from Rendering import Rendering
from UI import UI
#from Pi import Pi
# from LearningSimulation import LearningSimulation
from Background import Background

import gc

class MainGame:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        
        self.screen_width = 800
        self.screen_height = 600
        #self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.car = Car(self.screen_width, self.screen_height,self)
        self.road = Road(self.screen_width, self.screen_height)
        self.background = Background(800,600)
        
        self.ui = UI(self)
        self.rendering = Rendering(self.screen, self.road, self.car,self.ui,self.background)
        #pygame.mixer.music.load("simple_harmony.mid")
        pygame.mixer.music.set_volume(0.55)
        pygame.mixer.music.load("race_main.wav")
        pygame.mixer.music.play(-1)
        self.sound_offroad = pygame.mixer.Sound("offroad.wav")
        self.sound_offroad.set_volume(0.30)

        self.role_timer = pygame.USEREVENT + 1  
        pygame.time.set_timer(self.role_timer, 3000) # 300 seconds interval for role swap
        
        self.running = True

        self.elapsedTime = 0

        self.secondscounter = 0
        self.seconds = 0

        self.halfsecondscounter = 0
        self.halfseconds = 0

        self.scores = 0
        self.btn_status_dict={}

        self.controlM = []
        self.change = False

        self.controlM = [self.car.accelerate,self.car.brake_or_drift,self.car.steer_left,self.car.steer_right]

        #self.Pi = PI(self) don't delete this!

        self.btn_status_dict['accelerator']=False
        self.btn_status_dict['steerer_left']=False
        self.btn_status_dict['brake_drift']=False
        self.btn_status_dict['steerer_right']=False

        self.willswaprole = False
        self.swapTime = 5

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == self.role_timer:
                # self.car.swap_roles()6
                pass

    def check_key_states(self):
        #keys = self.Pi.read_input() #dont delete this!
        self.keys = pygame.key.get_pressed()

        self.btn_status_dict['accelerator']=False
        self.btn_status_dict['steerer_left']=False
        self.btn_status_dict['brake_drift']=False
        self.btn_status_dict['steerer_right']=False
        
        if self.keys[pygame.K_m]:
            print("Pause")
        if self.keys[pygame.K_w]:
            self.call_control_method("accelerator", self.controlM[0])
            self.btn_status_dict['accelerator']=True
        if self.keys[pygame.K_SPACE]:
            self.call_control_method("brake_drift", self.controlM[1])
            self.btn_status_dict['brake_drift']=True
        if self.keys[pygame.K_a] and not self.keys[pygame.K_d]:
            self.call_control_method("steerer_left", self.controlM[2])
            self.btn_status_dict['steerer_left']=True
        if self.keys[pygame.K_d] and not self.keys[pygame.K_a]:
            self.call_control_method("steerer_right", self.controlM[3])
            self.btn_status_dict['steerer_right']=True

    def call_control_method(self, role_name, method):
        #if any(role["name"] == role_name for role in self.car.roles):
            method()

    def update(self):
        if self.ui.game_state == "running":
            self.car.update()
        self.car.is_onroad(self.rendering)


        if self.car.isonroad and not self.car.ispartiallyoffroad:
            #self.Pi.stopvibrate()
            #print("StopVib")
            pass
        else:
            #print("Vib")           
            pass
            #self.Pi.vibrate()

        # print("On road: ",self.car.isonroad," Partially off road: ",self.car.ispartiallyoffroad)
        # self.road.update() # ideally I would like a cyclic array to store the road points and update them here so we can save memory.
        self.ui.update()
        # print(self.car.status())

    def render(self):
        self.rendering.draw_objects()

    def lateUpdate(self):
        self.rendering.lateUpdate()

    def updateScore(self):
        score = 0
        if self.car.isonroad:
            if self.car.move: score = 1
            else: score=0
        else :
            score = -1
        self.scores += score
        if self.scores<=0: self.scores=0

    def state_check(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] :
            quit()
        if keys[pygame.K_u] and self.ui.game_state == "start": 
            self.ui.game_state="running"
            self.running=True
            return
        if keys[pygame.K_u] and self.ui.game_state == "running" and self.elapsedTime>3000: 
            self.ui.game_state="restart"
            return
        if keys[pygame.K_u] and self.ui.game_state == "end": 
            self.ui.game_state="restart"
            return
        if self.car.position[1]<self.road.road_end_position[1]+450 or self.car.HP<=0:
            self.ui.game_state="end"
            return


    def run(self):
        clock = pygame.time.Clock()
        while True:
            
            self.state_check()
            if self.ui.game_state=="restart" : 
                break
            while self.running:
                self.handle_events()
                self.check_key_states()
                self.update()
                self.lateUpdate()      
                ms = self.clock.tick(90)
                fps = self.clock.get_fps()

                self.elapsedTime += ms
                self.secondscounter += ms

                if self.ui.game_state == "running":
                    if self.secondscounter>1000:
                        self.secondscounter = 0   
                        self.seconds+=1
                        self.change=True
                        self.updateScore()
                    if (self.seconds+2)%self.swapTime==0:
                        self.willswaprole = True
                    if self.seconds%self.swapTime == 0:
                        if self.seconds > 0 and self.change:
                            self.car.swap_roles()
                            self.controlM = [self.controlM[-1]] + self.controlM[:-1]
                            self.change = False
                            self.willswaprole = False
                break
            self.render()   

if __name__ == "__main__":

    while True:
        game = MainGame()
        game.run()
        gc.collect()

