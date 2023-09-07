# Rendering.py
import pygame
import numpy as np

class Rendering:
    def __init__(self, screen, road, car):
        self.screen = screen
        self.road = road
        self.car = car

        self.bg_color = (0, 128, 0)  # Background color
        self.road_color = (0, 0, 0)  # Road color 
        self.car_width = 20
        self.car_height = 40
        self.static_road_path = []

        self.road_texture = pygame.image.load('Pixel_Art/road_1.jpg')

        # Create a car surface at initialization to reuse in each frame
        self.car_surface = pygame.Surface((self.car.car_width, self.car.car_height))
        
        # Render the background once
        self.background = pygame.Surface(screen.get_size())
        self.background.fill(self.bg_color)

    def draw_objects(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_road()
        self.draw_car()
        pygame.display.flip()

    def draw_road(self):
        left_border, center_line, right_border = self.road.get_road_points()
        pygame.draw.lines(self.screen, (0, 0, 0), False, np.transpose(center_line), 2)
        pygame.draw.lines(self.screen, (255, 255, 255), False, np.transpose(left_border), 2)
        pygame.draw.lines(self.screen, (255, 255, 255), False, np.transpose(right_border), 2)

        polygon_points = np.concatenate((np.transpose(left_border), np.transpose(right_border)[::-1]), axis=0)
        pygame.draw.polygon(self.screen, self.road_color, polygon_points)

    def draw_road_texture(self):
        # TODO: Implement texture rendering for the road, jpg image is already loaded in self.road_texture
        pass

    def draw_car(self):
        self.car.draw(self.screen)

