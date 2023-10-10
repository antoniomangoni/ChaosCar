from shapely.geometry import Point, Polygon
import numpy as np
import pygame
from math import sin, cos, radians

class Car:
    def __init__(self, screen_width, screen_height):
        self.car_width = 128
        self.car_height = 128
        self.position = [screen_width // 2, screen_height - self.car_height]

        self.velocity = np.array([0.0, 0.0])
        self.max_velocity = 2
        self.max_delta_speed = 0.4
        self.smoothing_factor = 0.8

        self.speed = 0.0
        self.max_speed = 3
        self.acceleration = 0
        self.max_acceleration = 0.4
        self.direction = np.array([0.0, 0.0])
        self.turning_radius = 2  
        self.wheel_angle = 0  
        self.friction = self.max_acceleration * 0.1
        
        self.drifting = False
        self.accelerating = False
        self.drift_duration = 0
        self.drift_speed_threshold = 1.5
        self.drift_angle_threshold = 0.6

        self.old_wheel_angle = 0
        self.relative_angle = 0
        self.delta_angle = 0.2 

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
        self.state = 0 # 0: on road, 1: partially off road, 2: completely off road
        self.friction_model = np.array([self.friction, self.friction * 1.5, self.friction * 2])

        self.previous_pos_x=0
        self.move = False
    def update(self):
        # Update state and friction
        self.update_state()
        self.update_friction()
        
        # print(f"state: {self.state}, Relative angle: {round(self.relative_angle, 3)}, Accelerating: {self.accelerating}, Friction: {round(self.friction, 3)}, Drifting: {self.drifting}, Speed: {round(self.speed), 3}, Acceleration: {round(self.acceleration, 3)}, Force: {round(self.acceleration - self.friction, 3)}")
        if self.accelerating:
            print(f"Direction: {round(self.direction[0], 3)}, {round(self.direction[1], 3)}, Speed: {round(self.speed, 3)}, Position: {round(self.position[0], 3)}, {round(self.position[1], 3)}")
        
        # Update relative angle for drift
        self.relative_angle = (self.wheel_angle - self.old_wheel_angle) * self.delta_angle + (1 - self.delta_angle) * self.relative_angle
        self.old_wheel_angle = self.wheel_angle

        # Update direction
        self.direction[0] = -sin(radians(self.wheel_angle))
        self.direction[1] = -cos(radians(self.wheel_angle))

        # Update speed and position when accelerating
        if self.accelerating:
            new_speed = min(self.max_speed, max(-self.max_speed, self.speed + self.acceleration))
            delta_speed = new_speed - self.speed
            delta_speed = max(-self.max_delta_speed, min(self.max_delta_speed, delta_speed))
            self.speed += delta_speed

            self.position += self.direction * self.speed

        if self.previous_pos_x == self.position[1]:
            self.move=False
        else: 
            self.move=True
        
        self.previous_pos_x = self.position[1]
        


        # Reset accelerating flag
        self.accelerating = False

        # Perform drift if conditions met, else reduce speed due to friction
        if self.drifting:
            if self.drifting_conditions():
                self.perform_drift()
            else:
                self.drifting = False
                self.speed -= self.speed * self.friction
        else:
            self.speed -= self.speed * self.friction

        # Update car image and rect
        self.car_image = self.rot_center(self.original_car_image, self.wheel_angle)
        self.car_rect = self.car_image.get_rect(center=self.position)

    def rot_center(self, image, angle):
        loc = image.get_rect().center  #rot_image is not defined 
        rot_sprite = pygame.transform.rotate(image, angle)
        rot_sprite.get_rect().center = loc
        return rot_sprite

    def apply_force(self):
        self.speed += self.acceleration

    def accelerate(self):
        self.acceleration = min(0.1, self.acceleration + 0.1)
        self.accelerating = True

    def update_friction(self):
        self.friction = self.friction_model[self.state]

    def velocity_norm(self, velocity):
        velocity_magnitude = np.linalg.norm(velocity)
        if velocity_magnitude > self.max_velocity:
            velocity = (velocity / velocity_magnitude) * self.max_velocity
        return self.velocity
    
    def direction_change(self) -> bool:
        new_direction_1 = np.array([-sin(radians(self.wheel_angle))])
        return (np.sign(new_direction_1) != np.sign(self.direction[0]))
    
    def perform_drift(self):
        ortho_direction = np.array([-self.direction[1], self.direction[0]])

        if self.relative_angle < 0:
            ortho_direction = -ortho_direction

        drift_factor = abs(self.relative_angle)

        # Compute the new speed with drifting in mind, considering friction and drift factors
        proposed_speed = self.speed - self.speed * self.friction * drift_factor
        
        # Limit the maximum change in speed
        delta_speed = proposed_speed - self.speed
        delta_speed = max(-self.max_delta_speed, min(self.max_delta_speed, delta_speed))
        
        self.speed += delta_speed

        # Compute the new direction, blending the drift direction and the car's current direction
        new_velocity = self.direction * self.speed + ortho_direction * self.speed * drift_factor
        self.velocity = (1 - self.smoothing_factor) * self.velocity + self.smoothing_factor * new_velocity

        # Update the position based on the effective velocity
        self.position += self.velocity_norm(self.velocity)

    """
    def direction_change(self) -> bool:
        new_direction = np.array([-sin(radians(self.wheel_angle)), -cos(radians(self.wheel_angle))])
        return not np.all(np.sign(new_direction) == np.sign(self.direction))
    """
    def brake_or_drift(self):
        if self.drifting_conditions():
            self.drifting = True
            self.perform_drift()
        else:
            self.drifting = False
            self.friction = self.friction_model[2] # this make braking off road not count, a small positive feedback loop

    def drifting_conditions(self):
        return self.speed > self.drift_speed_threshold and abs(self.relative_angle) > self.drift_angle_threshold

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
    
    def update_state(self):
        if(self.isonroad and not self.ispartiallyoffroad):
            self.state = 0
            # print("On road")
        elif(self.isonroad and self.ispartiallyoffroad):
            self.state = 1
            # print("Partially off road")
        else: #
            self.state = 2
            self.drifting = False
            # print("Off road")

    def is_onroad(self, render):
        obb = self.create_obb(render)
        road_poly = Polygon(render.road_polygon_points)
        self.isonroad = self.check_obb_intersection(obb, road_poly)
        self.ispartiallyoffroad = self.check_corner_points(obb, road_poly)

    # (Oriented Bounding Box)
    def create_obb(self, render):
        length = 40
        width = 20
        pdir = np.array([-self.direction[1], self.direction[0]])
        leftuppoint = np.array(render.offset) + np.array(self.direction) * length + pdir * width
        leftbottompoint = np.array(render.offset) - np.array(self.direction) * length + pdir * width
        rightuppoint = np.array(render.offset) + np.array(self.direction) * length - pdir * width
        rightbottompoint = np.array(render.offset) - np.array(self.direction) * length - pdir * width
        obb = Polygon([leftuppoint, leftbottompoint, rightbottompoint, rightuppoint])
        return obb

    def check_obb_intersection(self, obb, road_poly):
        return obb.intersects(road_poly)

    def check_corner_points(self, obb, road_poly):
        # return all(corner.within(road_poly) for corner in obb.exterior.coords[:-1])
        return all(Point(corner).within(road_poly) for corner in obb.exterior.coords[:-1])

    def is_onroad(self, render):
        obb = self.create_obb(render)
        road_poly = Polygon(render.road_polygon_points)
        self.isonroad = self.check_obb_intersection(obb, road_poly)
        self.ispartiallyoffroad = not self.check_corner_points(obb, road_poly)
