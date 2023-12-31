import pygame
import numpy as np
import pygame.gfxdraw
from Plants import Plants
WHITE = (225,225,225)
class Rendering:
    def __init__(self, screen, road, car, ui,background,game):
        self.game = game
        self.screen = screen
        self.road = road
        self.car = car

        self.bg_color = (0, 128, 0)  # Background color
        self.road_color = (0, 0, 0)  # Road color 
        self.car_width = 20
        self.car_height = 40
        self.static_road_path = []

        self.screen_width=800
        self.screen_height=600
        self.road_texture = pygame.image.load('Pixel_Art/road_2.jpg')
        self.road_texture=self.road_texture.convert()

        # Create a car surface at initialization to reuse in each frame
        self.car_surface = pygame.Surface((self.car.car_width, self.car.car_height))

        # Create a road surface at initialization to reuse in each frame
        self.road_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        # Get road control point to render
        self.right_border, self.left_border = self.road.get_road_points()
        self.road_polygon_points=[]

        # Render the background once
        self.background = background
        self.plants = Plants(self.screen_width,self.screen_height,self.road,self)

        # camera parameters
        self.blackbackground = pygame.Surface(screen.get_size())
        self.blackbackground.fill((0,0,0))
        self.pos = self.car.position
        self.offset = [400,400]
        
        # ui
        self.ui = ui
        self.start_surface = pygame.image.load('Pixel_Art/startmenuimage.png')
        self.start_surface = pygame.transform.scale(self.start_surface, (800, 600))

        #enemy
        self.enemy = self.game.enemy

    def lateUpdate(self):
        self.pos = self.car.position
        #print(self.pos)
    
    def draw_objects(self):
        #self.screen.blit(self.blackbackground, (0, 0))

        # when draw something at (x,y)
        # , need draw at (x-self.pos[0] + self.offset[0],y-self.pos[1] + self.offset[1])


        if self.ui.game_state == 'start': 
            #self.draw_ui()
            self.screen.blit(self.start_surface,(0,0))

            if self.ui.game.elapsedTime%200 > 100:
                self.ui.tipimg = self.ui.tipfont.render('PRESS WHITE BUTTON', True, WHITE)
                self.screen.blit(self.ui.tipimg, (400 - self.ui.tipimg.get_width() // 2, 490 - self.ui.tipimg.get_height() // 2))
                self.ui.tipimg = self.ui.tipfont.render('TO START!', True, WHITE)
                self.screen.blit(self.ui.tipimg, (400 - self.ui.tipimg.get_width() // 2, 535 - self.ui.tipimg.get_height() // 2))
            pygame.display.flip()
            return
        self.draw_background()
        self.draw_road()
        self.draw_car()
        self.draw_enemy()
        self.draw_ui()

        pygame.display.flip()
    
    def draw_ui(self):
        self.ui.render(self)

    def draw_road(self):
        _left_border = [0,0]
        _right_border = [0,0]

        _left_border = np.array(self.left_border) - self.pos + self.offset
        _right_border = np.array(self.right_border) - self.pos + self.offset
        #_left_border=[(x-self.pos[0] + self.offset[0], y - self.pos[1] + self.offset[1]) for x, y in self.left_border]
        #_right_border=[(x-self.pos[0] + self.offset[0], y - self.pos[1] + self.offset[1]) for x, y in self.right_border]
        
        #get road point
        self.road_polygon_points = np.concatenate((self.visible(_left_border),self.visible(_right_border)[::-1]),axis=0)

        #clear screen
        self.road_surface.fill((0,0,0,0))

        #need?
        #pygame.draw.lines(self.road_surface,(0,0,0),False,_left_border,2)
        #pygame.draw.lines(self.road_surface,(0,0,0),False,_right_border,2)
        m=np.random.randint(0,15)
        n=np.random.randint(0,15)
        
        if self.renderable(self.road_polygon_points): pygame.gfxdraw.textured_polygon(self.road_surface, self.road_polygon_points, self.road_texture,-int(self.pos[0]),int(self.pos[1]))
        #pygame.draw.polygon(self.road_surface, (0, 0, 0), self.road_polygon_points)
        self.screen.blit(self.road_surface,(0,0))


    def renderable(self, point):
        if np.size(point) == 0 : return False
        a=np.min(point,axis=0)
        b=np.max(point,axis=0)
        if b[0] <= 5:
            return False
        if a[0] >=795:
            return False
        return True
    

    def visible(self,road_point):
        screen_min_y=self.offset[1]-500
        screen_max_y=350+self.offset[1]
        visible_border=road_point

        num=[]
        for i in range(len(visible_border)):
            if visible_border[i][1]>screen_max_y or visible_border[i][1]<screen_min_y:
                num.append(i)

        visible_border=np.delete(visible_border,num[:], 0)
        return visible_border
    
    def draw_road_texture(self):
        pass

    def draw_car(self):
        self.car.draw(self.screen,self)

    def draw_background(self):
        self.background.draw(self.screen,self)
        self.plants.draw(self.screen,self)

    def draw_enemy(self):
        self.enemy.draw(self.screen,self)
