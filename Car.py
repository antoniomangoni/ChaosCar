from math import cos, sin, radians
import pygame

class Car:
    def __init__(self, screen_width, screen_height):
        self.car_width = 128
        self.car_height = 128
        self.position = [screen_width // 2, screen_height - self.car_height]  

        self.speed = 0
        self.velocity = [0, 0]
        self.max_speed = 5
        self.acceleration = 0
        self.max_acceleration = 0.1
        self.direction = 0  
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

    def update(self):
        
        self.wheel_angle -= self.wheel_angle * self.friction  # Apply friction to the wheels
        self.direction += self.wheel_angle * (self.speed / 50.0)  # Adjusted turning dynamics

        self.speed -= self.speed * (1 * self.friction)

        # Rotate the car image by the updated direction
        self.car_image = pygame.transform.rotate(self.original_car_image, -self.direction)
        self.car_rect = self.car_image.get_rect(center=(self.position[0] + self.car_width // 2, self.position[1] + self.car_height // 2))

        self.car_rect.topleft = (self.position[0], self.position[1])

        self.speed = min(self.max_speed, max(-self.max_speed, self.speed + self.acceleration))
        self.position[0] += self.speed # * cos(radians(self.direction))
        self.position[1] -= self.speed # * sin(radians(self.direction))
        
        self.acceleration = 0

    def update2(self):
        
        self.direction += self.wheel_angle # * (self.speed / 50.0)

        self.speed -= self.speed * (1 * self.friction)

        # Rotate the car image by the updated direction
        self.car_image = pygame.transform.rotate(self.original_car_image, -self.direction)
        self.car_rect = self.car_image.get_rect(center=(self.position[0] + self.car_width // 2, self.position[1] + self.car_height // 2))

        self.car_rect.topleft = self.position

        self.speed = min(self.max_speed, max(-self.max_speed, self.speed + self.acceleration))
        self.position[0] += self.speed # * cos(radians(self.direction))
        self.position[1] -= self.speed # * sin(radians(self.direction))
        
        self.acceleration = 0

    def apply_force(self):
        self.speed += self.acceleration

    def accelerate(self):
        self.acceleration = min(0.1, self.acceleration + 0.1)
    
    def brake_or_drift(self):
        self.acceleration = max(-0.1, self.acceleration - 0.1)

    def steer_left(self):
        if self.wheel_angle > -15:  
            self.wheel_angle -= 1

    def steer_right(self):
        if self.wheel_angle < 15:  
            self.wheel_angle += 1

    def swap_roles(self):
        self.roles = [self.roles[-1]] + self.roles[:-1]

    def draw(self, screen):
        screen.blit(self.car_image, self.car_rect.topleft)

    def get_rect(self):
        return self.rect
