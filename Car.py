from math import cos, sin, radians
import numpy as np
import pygame

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

    def rot_center(self, image, angle):
        loc = image.get_rect().center  #rot_image is not defined 

        rot_sprite = pygame.transform.rotate(image, angle)

        rot_sprite.get_rect().center = loc

        return rot_sprite
    
    def update(self):
        
        self.direction[0] = -sin(radians(self.wheel_angle))
        self.direction[1] = -cos(radians(self.wheel_angle))

        self.speed = min(self.max_speed, max(-self.max_speed, self.speed + self.acceleration))
        self.position += self.direction * self.speed

        self.speed -= self.speed * (1 * self.friction)
        self.acceleration = 0
        print(self.direction, self.speed, self.wheel_angle)

        # Render Update: Rotate the car image by the updated direction
        self.car_image = self.rot_center(self.original_car_image, self.wheel_angle)
        self.car_rect = self.car_image.get_rect(center=self.position)
        

    def apply_force(self):
        self.speed += self.acceleration

    def accelerate(self):
        self.acceleration = min(0.1, self.acceleration + 0.1)
    
    def brake_or_drift(self):
        self.acceleration = max(-0.1, self.acceleration - 0.1)

    def steer_left(self):
            self.wheel_angle = (self.wheel_angle + 1)%360

    def steer_right(self):
            self.wheel_angle = (self.wheel_angle - 1)%360

    def swap_roles(self):
        self.roles = [self.roles[-1]] + self.roles[:-1]

    def draw(self, screen):
        screen.blit(self.car_image, self.car_rect)

    def get_rect(self):
        return self.rect
