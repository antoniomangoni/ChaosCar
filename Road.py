import pygame
from scipy.interpolate import splprep, splev
import numpy as np

class Road:
    def __init__(self, screen_width, screen_height, control_point_variance=600, road_width=150, road_length=30):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.control_points=[]
        self.control_point_variance = control_point_variance
        self.road_width = road_width
        self.road_end_position=[0,0]
        #add start
        self.control_points.append((500,900))
        self.control_points.append((500,200))
        self.control_points.append((500,0))

        #road point position
        self.road_min_x=0
        self.road_max_x=0
        self.road_min_y=0
        self.road_max_y=0

        for i in range(3,road_length):
            n=i%3
            m=((np.random.randint(-self.screen_width, self.screen_width)*n),-150*i)
            self.control_points.append(m)
        
        self.road_end_position=self.control_points[-1]

        self.control_points.append((self.control_points[-1][0],-150*(road_length+3)))

    def calculate_bezier(self, points, t):
        n = len(points) - 1
        x, y = 0, 0
        for i, (px, py) in enumerate(points):
            coef = np.math.comb(n, i) * (1 - t) ** (n - i) * t ** i
            x += coef * px
            y += coef * py
        return x, y


    def get_road_points(self, num_points=150):
        right_border=[]
        left_border=[]

        for i in range(num_points):
            t = i / num_points
            x, y = self.calculate_bezier(self.control_points, t)
            right_border.append((int(x), int(y)))

        for i in range(1, len(right_border) - 1):
            x1, y1 = right_border[i - 1]
            x2, y2 = right_border[i]
            x3, y3 = right_border[i + 1]

            tangent_x = x2 - x1, y2 - y1
            tangent_length = np.sqrt(tangent_x[0] ** 2 + tangent_x[1] ** 2)
            unit_tangent_x = tangent_x[0] / tangent_length, tangent_x[1] / tangent_length

            normal_x = unit_tangent_x[1], -unit_tangent_x[0]

            new_x = x2 + self.road_width * normal_x[0]
            new_y = y2 + self.road_width * normal_x[1]
            left_border.append((int(new_x), int(new_y)))

        all_border=np.concatenate((left_border,right_border),axis=0)
        all_border=np.transpose(all_border)
        self.road_min_x=np.min(all_border[0])
        self.road_max_x=np.max(all_border[0])
        self.road_min_y=np.min(all_border[1])
        self.road_max_y=np.max(all_border[1])

        return right_border,left_border

    def road_pixel_set(self):
        
        pass
    



