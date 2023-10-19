import pygame
from scipy.interpolate import splprep, splev
import numpy as np
from math import factorial
from scipy.interpolate import CubicSpline

class Road:
    def __init__(self, screen_width, screen_height, control_point_variance=600, road_width=150, road_length=60):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.control_points=[]
        self.control_point_variance = control_point_variance
        self.road_width = road_width
        self.road_end_position=[0,0]
        #add start
        
        self.control_points.append((500,600))
        self.control_points.append((500,300))
        self.control_points.append((500,0))

        #road point position
        self.road_min_x=0
        self.road_max_x=0
        self.road_min_y=0
        self.road_max_y=0
        self.all_border=0

        for i in range(3,road_length,3):
            if i == 3 or i ==6 :
                self.control_points.append((500,-300*i))
                self.control_points.append((700,-300*(i+1)))
                self.control_points.append((400,-300*(i+2)))
            else:
                self.control_points.append((500,-300*i))
                self.control_points.append(((np.random.randint(500, self.screen_width-100)),-300*(i+1)))
                self.control_points.append(((np.random.randint(-250, 500)),-300*(i+2)))
        
        self.control_points.append((self.control_points[-1][0],-300*(road_length+3)))

        self.road_end_position=self.control_points[-1]


    def edge_modification(self, left_border, index_start, index_end, normals_border):
       
        #o=int((index_start+index_end)/2)+3
        o=index_end-6
        num = (index_end-index_start+1)
        
        P = lambda t: (1 - t)**2 * left_border[index_start] + 2 * t * (1 - t) * normals_border[o] + t**2 * left_border[index_end]
        edge_points = np.array([P(t) for t in np.linspace(0, 1, num)])
        return num, edge_points


    def get_road_points(self, num_points=1000):
        right_border=[]
        left_border=[]
        normals_border=[]


        t=np.arange(len(self.control_points))
        cs=CubicSpline(t,self.control_points,bc_type='natural')

        right_border=np.array([cs(i) for i in np.linspace(0, len(self.control_points)-1, num_points)])

        #normal for right border
        tangents = cs.derivative()(np.linspace(0, len(self.control_points) - 1, num_points))
        normals = np.array([-tangents[:, 1], tangents[:, 0]])

        #offset
        offset_distance = -self.road_width 

        new_border=offset_distance * (normals / np.linalg.norm(normals, axis=0))
        left_border = right_border + np.transpose(new_border)


        #offset for left border
        tangents = cs.derivative()(np.linspace(0, len(self.control_points) - 1, num_points))
        normals = np.array([-tangents[:, 1], tangents[:, 0]])

        offset_distance = - 150  
        new_border=offset_distance * (normals / np.linalg.norm(normals, axis=0))
        normals_border = right_border + np.transpose(new_border)


        index_start = 1
        index_end = 0
        while True:
            if left_border[index_start][1]>left_border[index_start-1][1]:
                index_end = index_start
                index_start += 1
                while left_border[index_start][1]>left_border[index_start-1][1]:
                    index_start+=1
                else : 
                    num, new_points = self.edge_modification(left_border, index_end-10, index_start+7, normals_border)
                    for i in range(0,num-1):
                        left_border[index_end-10+i] = new_points[i]

            else: index_start+=1

            if index_start == len(left_border): break
            else: continue


        self.all_border=np.concatenate((left_border,right_border),axis=0)
        self.all_border=np.transpose(self.all_border)

        self.road_min_x=np.min(self.all_border[0])
        self.road_max_x=np.max(self.all_border[0])
        self.road_min_y=np.min(self.all_border[1])
        self.road_max_y=np.max(self.all_border[1])

        return right_border,left_border
        
    def polygon_pointer(self):
        return self.all_border

    def road_pixel_set(self):
        pass
