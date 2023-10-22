import pygame
import numpy as np
from Car import Car
from Road import Road
from Rendering import Rendering
from UI import UI
#from Pi import PI
from Background import Background

class MainGame:
    def __init__(self, switch=True):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.switch = switch
        self.screen_width = 800
        self.screen_height = 600
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
        self.sound_offroad.set_volume(0.35)

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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == self.role_timer:
                # self.car.swap_roles()6
                pass

    def check_key_states(self):
        #keys = self.Pi.read_input() #dont delete this!
        keys = pygame.key.get_pressed()

        self.btn_status_dict['accelerator']=False
        self.btn_status_dict['steerer_left']=False
        self.btn_status_dict['brake_drift']=False
        self.btn_status_dict['steerer_right']=False
        
        if keys[pygame.K_m]:
            print("Pause")
        if keys[pygame.K_w]:
            self.call_control_method("accelerator", self.controlM[0])
            self.btn_status_dict['accelerator']=True
        if keys[pygame.K_SPACE]:
            self.call_control_method("brake_drift", self.controlM[1])
            self.btn_status_dict['brake_drift']=True
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.call_control_method("steerer_left", self.controlM[2])
            self.btn_status_dict['steerer_left']=True
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.call_control_method("steerer_right", self.controlM[3])
            self.btn_status_dict['steerer_right']=True

    def call_control_method(self, role_name, method):
        #if any(role["name"] == role_name for role in self.car.roles):
            method()

    def update(self):
        if self.ui.game_state:
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
        self.scores += self.getStepScore()
    
    def getStepScore(self):
        score = 0
        if self.car.isonroad:
            if self.car.move:
                score = 0.1
                if self.car.drifting:
                    score += 0.2
            else: score=0
        elif self.scores>0:
            score = -0.075
        return score
    
    def getScreen(self):
        return pygame.surfarray.array3d(self.screen)
    
    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.check_key_states()
            self.update()
            self.render()   
            self.lateUpdate()      
            ms = self.clock.tick(90)
            fps = self.clock.get_fps()
            if fps < 90:
                pass
                #print(fps)

            self.elapsedTime += ms
            self.secondscounter += ms
            self.updateScore()
           
            if self.ui.game_state:
                if self.secondscounter>1000:
                    self.secondscounter = 0   
                    self.seconds+=1
                    self.change=True
                    self.updateScore()
                if self.seconds%15 == 0 and self.switch == True:
                    if self.seconds > 0 and self.change:
                        self.car.swap_roles()
                        self.controlM = [self.controlM[-1]] + self.controlM[:-1]
                        self.change = False

        pygame.quit()

if __name__ == "__main__":
    game = MainGame()
    game.run()
