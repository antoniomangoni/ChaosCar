import pygame
from math import cos, sin, radians
import numpy as np

class Car:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.car_width = 80
        self.car_height = 100
        self.x = screen_width // 2 - self.car_width // 2
        self.y = screen_height - self.car_height - 10
        self.speed = 0
        self.angle = 90
        self.image = pygame.image.load('Pixel_Art/car_blue_pixel.png')
        self.image = pygame.transform.scale(self.image, (self.car_width, self.car_height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def accelerate(self):
        self.speed += 0.1

    def brake_or_drift(self):
        self.speed -= 1
        if self.speed < 0:
            self.speed = 0

    def steer_left(self):
        self.angle += 5
        self.image = pygame.transform.rotate(self.image, 5)
        self.rect = self.image.get_rect(center=self.rect.center)

    def steer_right(self):
        self.angle -= 5
        self.image = pygame.transform.rotate(self.image, -5)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.x += self.speed * cos(radians(self.angle))
        self.y -= self.speed * sin(radians(self.angle))
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Test script to check if the Car.py works well. You can remove it later.
if __name__ == "__main__":
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    car = Car(screen_width, screen_height)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            car.accelerate()
        if keys[pygame.K_s]:
            car.brake_or_drift()
        if keys[pygame.K_a]:
            car.steer_left()
        if keys[pygame.K_d]:
            car.steer_right()

        car.update()
        screen.fill((0, 128, 0))
        car.draw(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    pygame.quit()
