import pygame
from scipy.interpolate import splprep, splev
import numpy as np
from Checkpoint import Checkpoint

class Road:
    def __init__(self, screen_width, screen_height, control_point_variance=400, road_width=130):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.control_point_variance = control_point_variance
        self.road_width = road_width
        self.road_points = []
        
        self.control_points = [
            (self.screen_width // 2, self.screen_height),
            (self.screen_width // 2 - np.random.randint(-self.control_point_variance, self.control_point_variance), self.screen_height // 2),
            (self.screen_width // 2, self.screen_height // 4),
            (self.screen_width // 2, 0)
        ]

        self.tck, self.u = splprep(np.transpose(self.control_points), u=None, s=0.0)

        self.chunks = np.empty(4, dtype=object) # Initialize an empty array to hold 4 chunks

        self.checkpoints = np.empty(4, dtype=object)
        self.checkpoint_count = 5
        self.checkpoints = np.empty(self.checkpoint_count, dtype=object)
        self.current_checkpoint_index = 0
        self.delta = 0.1
        self.create_initial_checkpoints()

    def create_initial_checkpoints(self):
        u_min, u_max = self.u.min(), self.u.max()
        u_values = np.linspace(u_min, u_max, self.checkpoint_count + 1)
        for i in range(self.checkpoint_count):
            x, y = splev(u_values[i], self.tck, der=0)
            self.checkpoints[i] = Checkpoint(x, y, self.road_width, 1, u_values[i])

    def advance_checkpoints(self):
        self.current_checkpoint_index = (self.current_checkpoint_index + 1) % self.checkpoint_count
        last_u = self.checkpoints[self.current_checkpoint_index].distance
        new_u = (last_u + self.delta) % 1 # Modulo 1 to keep it within the 0-1 range for Bézier curves
        x, y = splev(new_u, self.tck, der=0)
        self.checkpoints[self.current_checkpoint_index] = Checkpoint(x, y, self.road_width, 1, new_u)

    def get_road_points(self, num_points=40):
        """Gets points along the Bezier curve and calculates points perpendicular to the curve for the road borders."""
        u_new = np.linspace(self.u.min(), self.u.max(), num_points)
        x, y = splev(u_new, self.tck, der=0)
        dx, dy = splev(u_new, self.tck, der=1)
        angle = np.arctan2(dy, dx)
        
        left_border_x = x + self.road_width / 2 * np.cos(angle + np.pi / 2)
        left_border_y = y + self.road_width / 2 * np.sin(angle + np.pi / 2)
        
        right_border_x = x - self.road_width / 2 * np.cos(angle + np.pi / 2)
        right_border_y = y - self.road_width / 2 * np.sin(angle + np.pi / 2)

        return (left_border_x, left_border_y), (x, y), (right_border_x, right_border_y)

