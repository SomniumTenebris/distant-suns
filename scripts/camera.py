import math
import core_functions as cfunc

class Camera():#Handles global variables
    def __init__(self, WIDTH, HEIGHT, g_locx, g_locy):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.error = 10
        self.SPEED = 1

        self.g_loc = [g_locx, g_locy]
       
    def recenter(self, player):
        screenCenter = (self.WIDTH/2, self.HEIGHT/2)
        delta_x, delta_y, distance, angle = cfunc.trig2(screenCenter, player.pos)

        angle = math.degrees(angle)
        angle = cfunc.bound(angle)
        angle = math.radians(angle)

        if distance >= self.error:
            self.g_loc[0] += -self.SPEED*math.sin(angle)
            self.g_loc[1] += self.SPEED*math.cos(angle)

    def update(self, player):
        g_locx, g_locy = self.g_loc
        if (player.x - g_locx) <= self.WIDTH/4 and player.velocity[0] < 0:
            g_locx += player.velocity[0]
        if (player.x - g_locx) >= 3*self.WIDTH/4 and player.velocity[0] > 0:
            g_locx += player.velocity[0]

        if (player.y + g_locy) <= self.HEIGHT/4 and player.velocity[1] < 0:
            g_locy -= player.velocity[1]
        if (player.y + g_locy) >= 3*self.HEIGHT/4 and player.velocity[1] > 0:
            g_locy -= player.velocity[1]

        self.g_loc = [g_locx, g_locy]
