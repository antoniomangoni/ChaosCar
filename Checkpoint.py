import pygame

class Checkpoint:
    def __init__(self, x, y, width, height, distance, active=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.distance = distance
        self.active = active
        self.colour = (255, 0, 0) # Red

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def new_location(self, pos):
        self.x = pos[0]
        self.y = pos[1]
    
    def collision_check(self, car_x, car_y):
        # Implement collision detection logic here
        pass
    
    def trigger_event(self):

        # Add score
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))

