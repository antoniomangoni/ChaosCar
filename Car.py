from math import cos, sin, radians
import numpy as np
import pygame
from shapely.geometry import Point, box, Polygon
class Car:
    def __init__(self, screen_width, screen_height):
        self.car_width = 128
        self.car_height = 128
        self.position = [screen_width // 2, screen_height - self.car_height]

        self.velocity = np.array([0.0, 0.0])

        self.speed = 0.0
        self.max_speed = 5
        self.acceleration = 0
        self.max_acceleration = 0.1
        self.direction = np.array([0.0, 0.0])
        self.turning_radius = 2  
        self.wheel_angle = 0  
        self.friction = self.max_acceleration / 2  

        self.drift_speed_threshold = 0.5
        self.drift_angle_threshold = 2

        self.original_car_image = pygame.image.load('Pixel_Art/car_blue_pixel.png')
        self.original_car_image = pygame.transform.scale(self.original_car_image, (self.car_width, self.car_height))
        self.car_image = self.original_car_image.copy()
        self.car_rect = self.car_image.get_rect(center=(screen_width//2, screen_height - self.car_height//2))

        self.roles = [
            {"name": "accelerator", "player": 1},
            {"name": "steerer_left", "player": 2},
            {"name": "steerer_right", "player": 3},
            {"name": "brake_drift", "player": 4}
        ]

        self.isonroad = True
        self.ispartiallyoffroad = False
        self.drifting = False
        self.status = 0 # 0: on road, 1: partially off road, 2: completely off road
        self.previous_pos=self.position
        self.move=False

    def rot_center(self, image, angle):
        loc = image.get_rect().center  #rot_image is not defined 

        rot_sprite = pygame.transform.rotate(image, angle)

        rot_sprite.get_rect().center = loc

        return rot_sprite
    
    def update(self):
        self.get_status()
        self.direction[0] = -sin(radians(self.wheel_angle))
        self.direction[1] = -cos(radians(self.wheel_angle))

        self.speed = min(self.max_speed, max(-self.max_speed, self.speed + self.acceleration))
        self.position += self.direction * self.speed
        
        if  self.position[0]==self.previous_pos[0] and self.position[1]==self.previous_pos[1]:
            self.move=False
        else:
            self.move=True
        #self.previous_pos=self.position

        self.speed -= self.speed * (1 * self.friction)
        self.acceleration = 0
        #print(self.direction, self.speed, self.wheel_angle)

        # Render Update: Rotate the car image by the updated direction
        self.car_image = self.rot_center(self.original_car_image, self.wheel_angle)
        self.car_rect = self.car_image.get_rect(center=self.position)

    def apply_force(self):
        self.speed += self.acceleration

    def accelerate(self):
        self.acceleration = min(0.1, self.acceleration + 0.1)
        
    
    def brake_or_drift(self):
        self.acceleration = max(-0.1, self.acceleration - 0.1)
        if self.speed > self.drift_speed_threshold and abs(self.wheel_angle) > self.drift_angle_threshold:
            self.perform_drift()

    def steer_left(self):
            self.wheel_angle = (self.wheel_angle + 1)%360

    def steer_right(self):
            self.wheel_angle = (self.wheel_angle - 1)%360

    def swap_roles(self):
        self.roles = [self.roles[-1]] + self.roles[:-1]

    def draw(self, screen, render):
        screen.blit(self.car_image, [self.car_rect.x-render.pos[0]+render.offset[0],self.car_rect.y-render.pos[1]+render.offset[1]])

    def get_rect(self):
        return self.rect
    
    def get_status(self):
        if(self.isonroad and not self.ispartiallyoffroad):
            self.status = 0
            # print("On road")
        elif(self.isonroad and self.ispartiallyoffroad):
            self.status = 1
            # print("Partially off road")
        else: #
            self.status = 2
            # print("Off road")

    def is_onroad(self,render):
        poly = Polygon(render.road_polygon_points)
        #centerpoint = Point(render.offset[0],render.offset[1])

        length = 40
        width = 20
        pdir = np.array(-self.direction[1],self.direction[0])
        leftuppoint = np.array(render.offset)+np.array(self.direction)*length+pdir*width
        leftuppoint = Point(leftuppoint[0],leftuppoint[1])
        leftbottompoint = np.array(render.offset)-np.array(self.direction)*length+pdir*width
        leftbottompoint = Point(leftbottompoint[0],leftbottompoint[1])

        rightuppoint = np.array(render.offset)+np.array(self.direction)*length-pdir*width
        rightuppoint = Point(rightuppoint[0],rightuppoint[1])
        rightbottompoint = np.array(render.offset)-np.array(self.direction)*length-pdir*width
        rightbottompoint = Point(rightbottompoint[0],rightbottompoint[1])

        obb = Polygon([leftuppoint,leftbottompoint,rightbottompoint,rightuppoint])

        #obb test
        self.isonroad = obb.intersects(poly)

        #corner point not on road
        self.ispartiallyoffroad = (not leftuppoint.within(poly)) or (not leftbottompoint.within(poly)) \
                               or (not rightbottompoint.within(poly)) or (not rightbottompoint.within(poly)) 
         
    def perform_drift(self):
        drift_angle = radians(self.wheel_angle)
        
        v_parallel = self.speed * cos(drift_angle)
        v_perpendicular = self.speed * sin(drift_angle)
        
        v_perpendicular += self.acceleration * sin(drift_angle)
        
        orientation_direction = np.array([cos(radians(self.wheel_angle)), sin(radians(self.wheel_angle))])
        drift_direction = np.array([-sin(radians(self.wheel_angle)), cos(radians(self.wheel_angle))])
        
        self.position += v_parallel * orientation_direction + v_perpendicular * drift_direction
