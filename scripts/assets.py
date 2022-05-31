import pygame
import math
import core_functions as cfunc
import global_vars as gbv
import projectiles as pjt

################
# Space Cannon #
################

class SpaceCannon(pygame.sprite.Sprite):#Dud class, just for collisions. NEED TO FIX This. Pos is where it's blitted, and shuold be where its collision is calculated tambien
    def __init__(self, x, y, angle = 360):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/images/misc/Space_Cannon_Body.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, .75)
        
        self.angle = angle
        self.x, self.y = x, y
        self.pos = [x, y]
        self.health = 100

        self.rect = self.image.get_rect()
        self.center_x,  self.center_y = self.rect[2]/2,self.rect[3]/2
     
        self.pos = [x+self.center_x, y+self.center_y]

        self.cannon = SpaceGun(self.x + 50, self.y - 100, self.angle, self.pos, 0)


    def update(self, g_loc, projectileList):
        g_locx, g_locy = g_loc
        self.cannon.blitRotate(g_loc)

        self.cannon.cooldown -= 1
        self.pos[0] = self.x - g_locx #Maybe can actually do multiple wih lists?
        self.pos[1] = self.y + g_locy

        self.rect.x, self.rect.y = self.pos[0]-self.center_x, self.pos[1]-self.center_y

        gbv.screen.blit(self.image, ([self.pos[0]-self.center_x, self.pos[1]-self.center_y]))
        self.cannon.x, self.cannon.y = self.x, self.y

        #pygame.draw.circle(screen, (100, 0 ,150), (self.pos), 5)


        self.cannon.tip = (self.pos[0] + math.cos(math.radians(self.cannon.angle) + math.pi/2) * self.cannon.LENGTH,
                           self.pos[1] - math.sin(math.radians(self.cannon.angle) + math.pi/2)*self.cannon.LENGTH) # Calculate the tip of the gun's position

        # Cannon shooting code
        if self.cannon.cooldown <= 0:
            self.cannon.cooldown = self.cannon.maxCooldown
            if self.cannon.canFire == True:
                self.cannon.shoot(projectileList, g_loc)

class SpaceGun(pygame.sprite.Sprite):#Actually moving part of gun
    def __init__(self, x, y, angle, pos, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/images/misc/Space_Cannon_Gun.png")
        self.image = pygame.transform.rotozoom(self.image, 0, .75)
        self.angle = angle
        self.radians = math.radians(self.angle)
        self.health = 0

        self.x, self.y = x, y

        self.canFire = False
        self.maxCooldown = 100
        self.cooldown = self.maxCooldown
        
        self.bound = [90, 270]

        
        self.rect = self.image.get_rect()
        self.center_x, self.center_y = self.rect[2]/2, self.rect[3] - 15 #Not actually center, so I can pivot better
        
        self.pos = pos
        self.pivot = [self.pos[0] + self.center_x, pos[1] + self.center_y]
        
        #-----Physics-----#
        
        self.MAXSPEED = .05
        self.ACCEL = .01
        self.ANGULARSPEED = 2
        self.SPACE = 10
        self.LENGTH = self.rect[3]*.7

        self.tip = (self.pivot[0] - math.sin(angle) * self.LENGTH, self.pivot[1] + math.cos(angle)*self.LENGTH)
        self.portA = (self.tip[0] + math.sin(angle)*self.SPACE, self.tip[1] + math.cos(angle)*self.SPACE)
        self.portB = (self.tip[0] - math.sin(angle)*self.SPACE, self.tip[1] - math.cos(angle)*self.SPACE)
     

    def target(self, target):
        pass

    def moveTo(self, target):#Call during each game loop
        delta_x, delta_y, distance, angle = cfunc.trig2(self.pos, target.pos)
        self.approachTurn(angle)
       
        
    def blitRotate(self, g_loc):
        cfunc.blitRotate(self, g_loc)
        
    def approachTurn(self, angle):#Find fastest path to angle, something's off with the final rotations
        angle = math.degrees(angle)
        error = 3.1
        self.canFire = False

        if self.angle + error > angle and self.angle - error < angle:
            self.canFire = True
            #if self.cooldown <= 0:
                #self.shoot(projectileList)
        else:
            if self.angle < angle:
                if abs(self.angle-angle)<180:
                    self.angle += self.ANGULARSPEED
                else:
                    self.angle -= self.ANGULARSPEED

            else:
                if abs(self.angle-angle)<180:
                    self.angle -= self.ANGULARSPEED
                else:
                    self.angle += self.ANGULARSPEED
                
            if self.angle > 360:
                self.angle -= 360
            if self.angle < 0:
                self.angle += 360

            if self.bound[0] < self.angle < 180:
                self.angle = 90

            if 180 <= self.angle < self.bound[1]:
                self.angle = 270

        angle = math.radians(self.angle) + math.pi/2
        self.portA = (self.tip[0] + math.sin(angle)*self.SPACE, self.tip[1] + math.cos(angle)*self.SPACE)
        self.portB = (self.tip[0] - math.sin(angle)*self.SPACE, self.tip[1] - math.cos(angle)*self.SPACE)

    def shoot(self, projectileList, g_loc):
        projectileList.add(pjt.Bullet(self.portA[0], self.portA[1], "Cannon", 10, self.angle, 20, g_loc))#I need to move the cannon's ports to a better location
        projectileList.add(pjt.Bullet(self.portB[0], self.portB[1], "Cannon", 10, self.angle, 20, g_loc))#I need to move the cannon's ports to a better location 
