import pygame
import random
import global_vars as gbv

#This method of drawing stars feels sooo inefficient

class Background():
    def __init__(self):

        self.width = gbv.width
        self.height = gbv.height
    
        self.num_stars1, self.num_stars2 = 1000, 1000
        self.stars1, self.stars2 = [], []
        

        for i in range(0, self.num_stars1):
            x = random.randint(-5000, 5000)#Size of a given sector
            y = random.randint(-5000, 5000)
            pos = [x, y]
            self.stars1.append(pos)

        for i in range(0, self.num_stars2):
            x = random.randint(-5000, 5000)#Size of a given sector
            y = random.randint(-5000, 5000)
            pos = [x, y]
            self.stars2.append(pos)

        self.star1_speed = 50
        self.star2_speed = 100

        self.x, self.y = 0, 0
    
    def update(self, g_loc):
        g_locx, g_locy = g_loc
        
        for i in range(0, len(self.stars1)):#Optimize to only draw circles within the view of the screen
            if self.width > self.stars1[i][0] - g_locx/100 > 0 and self.height > self.stars1[i][1] - g_locy/100 > 0:
                pygame.draw.circle(gbv.screen, (255,255,255), (self.stars1[i][0] - g_locx/self.star1_speed,
                                                               self.stars1[i][1] + g_locy/self.star1_speed), 3)
                
        for i in range(0, len(self.stars2)):#Optimize to only draw circles within the view of the screen
            if self.width > self.stars2[i][0] - g_locx/100 > 0 and self.height > self.stars2[i][1] - g_locy/100 > 0:
                pygame.draw.circle(gbv.screen, (150,175,255), (self.stars2[i][0] - g_locx/self.star2_speed,
                                                               self.stars2[i][1] + g_locy/self.star2_speed), 2)
