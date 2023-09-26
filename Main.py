# Main.py
import pygame
import numpy as np
from Car import Car
from Road import Road
from Rendering import Rendering
# from LearningSimulation import LearningSimulation

class MainGame:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        self.car = Car(self.screen_width, self.screen_height)
        self.road = Road(self.screen_width, self.screen_height)
        
        self.rendering = Rendering(self.screen, self.road, self.car)
        pygame.mixer.music.load("simple_harmony.mid")
        pygame.mixer.music.play(-1)

        # self.learning_simulation = LearningSimulation()
        
        self.role_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.role_timer, 3000) # 300 seconds interval for role swap
        
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == self.role_timer:
                # self.car.swap_roles()
                pass

    def check_key_states(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.call_control_method("accelerator", self.car.accelerate)
        if keys[pygame.K_s]:
            self.call_control_method("brake_drift", self.car.brake_or_drift)
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.call_control_method("steerer_left", self.car.steer_left)
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.call_control_method("steerer_right", self.car.steer_right)

    def call_control_method(self, role_name, method):
        if any(role["name"] == role_name for role in self.car.roles):
            method()

    def update(self):
        self.car.update()
        self.car.is_onroad(self.rendering)
        # print("On road: ",self.car.isonroad," Partially off road: ",self.car.ispartiallyoffroad)
        # self.road.update() # ideally I would like a cyclic array to store the road points and update them here so we can save memory.

    def render(self):
        self.rendering.draw_objects()

    def lateUpdate(self):
        self.rendering.lateUpdate()

    def run(self):

        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.check_key_states()
            self.update()
            self.render()   
            self.lateUpdate()      
            self.clock.tick(100)
            print(self.clock.get_fps())
        
        
        pygame.quit()
if __name__ == "__main__":
    game = MainGame()
    game.run()
