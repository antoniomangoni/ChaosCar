# Rendering.py
import pygame
import numpy as np
from Background import Background

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
        self.background = Background(800,600)

        # camera parameters
        self.blackbackground = pygame.Surface(screen.get_size())
        self.blackbackground.fill((0,0,0))
        self.pos = self.car.position
        self.offset = [400,400]

        # road points
        self.left_border, self.center_line, self.right_border = self.road.get_road_points()
        self.road_polygon_points=[]

        
        
    def lateUpdate(self):
        self.pos = self.car.position

    
    def draw_objects(self):
        self.screen.blit(self.blackbackground, (0, 0))

        #when draw something at (x,y)
        # , need draw at (x-self.pos[0] + self.offset[0],y-self.pos[1] + self.offset[1])
        self.draw_background()
        self.draw_road()
        self.draw_car()
        pygame.display.flip()
        
    def draw_road(self):

        _left_border = [0,0]
        _right_border = [0,0]
        _center_line = [0,0]

        _left_border[0] = self.left_border[0] - self.pos[0] + self.offset[0]
        _left_border[1] = self.left_border[1] - self.pos[1] + self.offset[1]
        _right_border[0] = self.right_border[0] - self.pos[0] + self.offset[0]
        _right_border[1] = self.right_border[1] - self.pos[1] + self.offset[1]

        #_center_line[0] = self.center_line[0] - self.pos[0] + self.offset[0]
        #_center_line[1] = self.center_line[1] - self.pos[1] + self.offset[1]

        #pygame.draw.lines(self.screen, (0, 0, 0), False, np.transpose(_center_line), 2)
        pygame.draw.lines(self.screen, (255, 255, 255), False, np.transpose(_left_border), 2)
        pygame.draw.lines(self.screen, (255, 255, 255), False, np.transpose(_right_border), 2)

        self.road_polygon_points = np.concatenate((np.transpose(_left_border), np.transpose(_right_border)[::-1]), axis=0)

        #pygame.draw.polygon(self.screen, self.road_color, self.road_polygon_points)
        poly_surface = pygame.Surface((800, 600), pygame.SRCALPHA)
        
        pygame.draw.polygon(poly_surface, (255, 255, 255), self.road_polygon_points)
        self.screen.blit(poly_surface,(0,0))

    def draw_road_texture(self):
        # TODO: Implement texture rendering for the road, jpg image is already loaded in self.road_texture
        pass

    def draw_car(self):
        self.car.draw(self.screen,self)

    def draw_background(self):
        self.background.draw(self.screen,self)

