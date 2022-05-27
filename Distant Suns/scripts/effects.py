import pygame
import math
import random
import global_vars as gbv

class Explosion():#Eventually add smoke and effects, but good for now.
    def __init__(self, pos, size):
        self.x = pos[0]
        self.y = pos[1]
        self.size = size

        self.duration = 20
        self.type = "" #Type indicates number of circles, color, and more

        self.radius1 = 20 * size
        self.radius2 = 20 * size
        self.radius3 = 20 * size
        self.radius4 = 20 * size


    def update(self, explosion_list):#Fine tune to look nicer
        pygame.draw.circle(gbv.screen, (255,0,0), (self.x, self.y), self.radius1)
        self.radius1 += 1.6 * self.size

        self.duration -= 1

        if self.duration <= 15:
            pygame.draw.circle(gbv.screen, (255,140, 0), (self.x, self.y), self.radius2)
            self.radius2 += 1.8 * self.size

        if self.duration <= 10:
            pygame.draw.circle(gbv.screen, (255,255, 0), (self.x, self.y), self.radius3)
            self.radius3 += 2.2 * self.size

        if self.duration <= 5:
            pygame.draw.circle(gbv.screen, (255,255, 255), (self.x, self.y), self.radius4)
            self.radius4 += 2.6 * self.size

        if self.duration <= 0:
            explosion_list.remove(self)
            del self

class Particle():
    def __init__(self, pos, angle, size, x_spread, y_spread, decay=0.25):
        self.pos = pos
        angle = math.radians(-angle)
        self.decay = decay
        
        self.velocity = [random.randint(*x_spread)/2, random.randint(*y_spread)/2] #not gonna work
        #self.velocity = self.velocity.magnitude() * math.cos(angle)
        self.velocity = [math.cos(angle)*self.velocity[0] - math.sin(angle)*self.velocity[1],
                         math.sin(angle)*self.velocity[0] + math.cos(angle)*self.velocity[1]]
        self.color = [255, 255, 255]
        #self.color = [random.randint(100, 255), random.randint(0, 255), random.randint(200, 255)]
        self.radius = random.randint(*size)

    def transition(self):
        speed_red = 10
        speed_green = 4
        if self.color[0] >= speed_red:
            self.color[0] -= speed_red
        if self.color[1] >= speed_green:
            self.color[1] -= speed_green
                
    def bounce(self):
        elasticity = 0.25
        self.velocity[0] *= -elasticity
        self.velocity[1] *= -elasticity
        self.update()

    def update(self):
        self.transition()
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        #self.velocity[1] += 0.5
        self.radius -= self.decay
        pygame.draw.circle(gbv.screen, self.color, self.pos, self.radius)

class Hyper_Line():
    def __init__(self, pos, angle, g_loc):
        self.x = pos[0] + random.randint(-20, 20) - math.cos(angle)*20
        self.y = pos[1] + random.randint(-15, 15) - math.sin(angle)*20
        self.speed = random.randint(1, 7)/4

        angle = math.radians(270-angle)
        self.angle = angle + random.randint(-5, 5)/40
        
        self.velocity = [math.cos(angle)*self.speed - math.sin(angle)*self.speed,
                         math.sin(angle)*self.speed + math.cos(angle)*self.speed]
        
        self.duration = random.randint(10, 20)
        self.scale = 20
        self.color = (255, 255, 255)

        self.g_loc = g_loc

        self.delta = self.speed

    def draw(self, g_loc):
        #g_locx = self.g_loc[0] - g_loc[0]
        #g_locy = self.g_loc[1] - g_loc[1]
        g_locx = self.delta*math.cos(self.angle)
        g_locy = self.delta*math.sin(self.angle)

        
        '''points = [
            [self.x + math.cos(self.angle) * self.speed * self.scale + g_locx,
             self.y + math.sin(self.angle) * self.speed * self.scale + g_locy],
            [self.x + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3 + g_locx,
             self.y + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3 + g_locy],
            [self.x - math.cos(self.angle) * self.speed * self.scale * 3.5 + g_locx,
             self.y - math.sin(self.angle) * self.speed * self.scale * 3.5 + g_locy],
            [self.x + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3 + g_locx,
             self.y - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3 + g_locy],
            ]'''

        points = [
            [self.x + math.cos(self.angle) * self.speed * self.scale + g_locx,
             self.y + math.sin(self.angle) * self.speed * self.scale + g_locy],
            [self.x + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3 + g_locx,
             self.y + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3 + g_locy],
            [self.x - math.cos(self.angle) * self.speed * self.scale * 3.5 + g_locx,
             self.y - math.sin(self.angle) * self.speed * self.scale * 3.5 + g_locy],
            [self.x + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3 + g_locx,
             self.y - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3 + g_locy]]
            
        pygame.draw.polygon(gbv.screen, self.color, points)

    def decelerate(self):
        if self.speed > 0.1:
            self.speed -= 0.1
        self.velocity = [math.cos(self.angle)*self.speed - math.sin(self.angle)*self.speed,
                         math.sin(self.angle)*self.speed + math.cos(self.angle)*self.speed]

    def update(self, g_loc, pos):
        self.decelerate()
        self.delta += self.speed
        
        #self.x += self.velocity[0]
        #self.y += self.velocity[1]
        self.x += pos[0]
        self.y += pos[1]
    
        self.draw(g_loc)


class Shake():
    def __init__(self, camera, duration):
        self.original_gloc = camera.g_loc
        self.duration = duration
    def shake(self):
        self.duration = None
        if self.duration > 0:
            pass
        
