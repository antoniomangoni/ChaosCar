import pygame
from Car import Car
from Road import Road
from Rendering import Rendering

class MainGame:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600))
        self.car = Car(800, 600)
        self.road = Road(800, 600)
        self.rendering = Rendering(self.screen, self.road, self.car)
        pygame.mixer.music.load("simple_harmony.mid")
        pygame.mixer.music.play(-1)
        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.car.check_key_states()
            self.car.update()
            self.rendering.draw_objects()
            self.rendering.lateUpdate()
            self.clock.tick(120)
            print(self.clock.get_fps())

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

if __name__ == "__main__":
    game = MainGame()
    game.run()

