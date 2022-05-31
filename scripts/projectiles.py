import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, origin, speed, angle, damage):#Origin is who shot the bullet
        pygame.sprite.Sprite.__init__(self)

        self.angle = angle
        
        self.image = pygame.image.load("data/images/misc/Bullet.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, self.angle + 90, .5)

        self.rect = self.image.get_rect()
        self.center_x, self.center_y = self.rect[2]/2, self.rect[3]/2


        self.pos = [x, y]
        self.rect.x, self.rect.y = self.pos[0] - self.center_x, self.pos[1] - self.center_y

        self.speed = 1
        self.life = 3000

        self.velocity = [-self.speed*math.sin(math.radians(self.angle)), -self.speed*math.cos(math.radians(self.angle))]

        self.radius = 5
        self.mass = 5

        self.origin = origin
        self.damage = damage

    def update(self, g_loc):
        
        self.velocity[0] = -self.speed*math.sin(math.radians(self.angle))
        self.velocity[1] = -self.speed*math.cos(math.radians(self.angle))

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.rect.x = self.pos[0] - self.center_x - g_loc[0]
        self.rect.y = self.pos[1] - self.center_y - g_loc[1]


        self.life -= 1

        if self.life <= 0:
            self.kill()
