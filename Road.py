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

        #add start
        self.control_points.append((500,900))
        self.control_points.append((500,200))
        self.control_points.append((500,0))

        for i in range(3,road_length):
            n=i%3
            m=((np.random.randint(-self.screen_width, self.screen_width)*n),-150*i)
            self.control_points.append(m)
            

        self.tck, self.u = splprep(np.transpose(self.control_points), u=None, s=0.0)


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
        return right_border,left_border

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
    



