import pygame
from scipy.interpolate import splprep, splev
import numpy as np

class Road:
    def __init__(self, screen_width, screen_height, control_point_variance=180, road_width=150):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.control_point_variance = control_point_variance
        self.road_width = road_width
        
        self.control_points = [
            (self.screen_width // 2 , self.screen_height+200),
            (self.screen_width // 2, self.screen_height+20),
            (self.screen_width // 2, self.screen_height//5*4),
            (self.screen_width // 2 - np.random.randint(-self.control_point_variance, self.control_point_variance), self.screen_height // 5*3),
            (self.screen_width // 2, self.screen_height//5),
            (self.screen_width // 2, -30),
            (self.screen_width // 2, -30-self.screen_height//5),
            (self.screen_width // 2 - np.random.randint(-self.control_point_variance*2, self.control_point_variance*2), -30-self.screen_height // 5*3),
            (self.screen_width , -30-self.screen_height//5*6),
            (self.screen_width // 2 - np.random.randint(-self.control_point_variance, self.control_point_variance), -30-self.screen_height // 5*8),
            (self.screen_width // 2, -30-self.screen_height//5*12),
            (self.screen_width // 3, -30-self.screen_height*3),
            (self.screen_width // 3, -30-self.screen_height*3.4),
            (self.screen_width // 2, -30-self.screen_height*4.3),
        ]

        self.tck, self.u = splprep(np.transpose(self.control_points), u=None, s=0.0)

    def get_road_points(self, num_points=80):
        """Gets points along the Bezier curve and calculates points perpendicular to the curve for the road borders."""
        u_new = np.linspace(self.u.min(), self.u.max(), num_points)

        x, y = splev(u_new, self.tck, der=0)
        dx, dy = splev(u_new, self.tck, der=1)
        angle = np.arctan2(dy, dx)
        
        left_border_x = x + self.road_width / 2 * np.cos(angle + np.pi / 2)
        left_border_y = y + self.road_width / 2 * np.sin(angle + np.pi / 2)

        right_border_x = x - self.road_width / 2 * np.cos(angle + np.pi / 2)
        right_border_y = y - self.road_width / 2 * np.sin(angle + np.pi / 2)


        for i in range(left_border_y.size):
            if i>0:
                if left_border_y[i]<left_border_y[i-1]:
                    continue
                else:
                    left_border_y[i]=left_border_y[i-1]+3

        for i in range(right_border_y.size):
            if i>0:
                if right_border_y[i]<right_border_y[i-1]:
                    continue
                else:
                    right_border_y[i]=right_border_y[i-1]+3

        #sort border but have a bug, wiating for fix
        #right_sort_index=(np.argsort(right_border_y))[::-1]
        #right_border_y=right_border_y[right_sort_index]
        #right_border_x=right_border_x[right_sort_index]


        return (left_border_x, left_border_y), (x, y), (right_border_x, right_border_y)

