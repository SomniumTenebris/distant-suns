import pygame, sys
import math
from spaceships import Spaceship
import global_vars as gbv
import core_functions as cfunc
from projectiles import Bullet

pygame.init()

class Enemy(Spaceship):
    def __init__(self, x, y, angle, speed, state):        
        self.image = pygame.image.load("data/images/ships/Enemy.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, .4)

        Spaceship.__init__(self, x, y, angle, speed)


        self.x = x
        self.y = y
        self.pos = [0,0]

        self.rect = self.image.get_rect()
        
        self.center_x = self.rect[2]/2
        self.center_y = self.rect[3]/2

        self.center = [self.rect.x + self.center_x, self.rect.y + self.center_y]

        self.width = self.rect[2]
        self.height = self.rect[3]
        self.radius = 40#Adjust in order to make easier to hit later on possibly

        self.angle = 0

        self.state = state
        self.state = "Travel"
        self.cooldown = 0
        self.health = 50

        self.closest = None
        self.closestDistance = 0

        self.orbitAngle = 0 #Eventually condense to the same value self.ManeuverAngle?
        self.loopAngle = 0
        self.change = 1
        self.reached = False #This is for moveTo; if the ship reaches its target position
        self.targetAngle = 0

        ###########
        # Physics #
        ###########
        self.angleSpeed = 0.01
        self.speed = 1
        self.velocity = [0, 0]
        self.correct = self.angleSpeed*self.speed
        self.orbitAngle2 = 0
        self.distance = None



        #--------Physics -----------#
        self.MAXSPEED = .05
        self.SPEED = 1.7
        self.ANGULARSPEED = 2
        self.ACCEL = .005

    def approachTurn(self, angle):#Find fastest path to angle, something's off with the final rotations
        error = 2
        if self.angle + error > angle and self.angle - error < angle:
            pass
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
                
                
            self.angle = cfunc.bound(self.angle)

    def moveTo(self, point):#Call during each game loop
        delta_x, delta_y, distance, angle = cfunc.trig2(self.center, point)#[self.rect.x, self.rect.y], point)
        angle = cfunc.bound(math.degrees(angle))

        self.approachTurn(angle)
        angle = math.radians(angle)

        self.velocity[0] = -self.SPEED*math.sin(angle)
        self.velocity[1] = -self.SPEED*math.cos(angle)

        error = 10
        if distance < error:
            self.velocity[0] = 0
            self.velocity[1] = 0
            self.reached = True
        else:
            self.reached = False

        pygame.draw.circle(gbv.screen, (0,255,0), (self.x, self.y), 10)
        pygame.draw.circle(gbv.screen, (255,0,0), (self.rect.x, self.rect.y), 10)

    def formOrbit(self, planet):
        x, y, distance, angle = cfunc.trig2(planet.pos, self.center)#[self.rect.x, self.rect.y])
        angle = math.degrees(angle)
        angle = cfunc.bound(angle)
        orbitDistance = 200
        
        pos = (planet.center[0], planet.center[1]) #**** it, fly right to the center of the **ing planet
        pygame.draw.circle(gbv.screen, (0,0,0), (pos), 10)

        if distance <= orbitDistance + planet.radius:
            self.state = "Orbit"
            self.orbitAngle = angle
        else:
            self.state = "Travel"

        self.moveTo(pos)

    def findNearestPlanet(self):
        dist = 10000000
        closest = None
        for i in masterCollide:
            x, y, distance, angle = cfunc.trig2(i.pos,[self.x, self.y])
            if distance < dist:
                closest = i           

    def circle(self, planet):
        angle = cfunc.trig3(self, planet)[2] #There's a way to improve this, as radius is changing, but it's good enough
        self.orbitAngle2 += self.angleSpeed
        
        self.velocity[0] = (self.distance) * math.sin(self.orbitAngle2) * self.correct
        self.velocity[1] = (self.distance) * math.cos(self.orbitAngle2) * self.correct
        
        self.approachTurn(180+math.degrees(math.atan2(self.velocity[0], self.velocity[1])))

    def goTo(self, planet):
        dx, dy, angle, distance = cfunc.trig3(self, planet)
        self.velocity[0] = math.cos(angle) * self.speed
        self.velocity[1] = math.sin(angle) * self.speed

        self.approachTurn(180+math.degrees(math.atan2(self.velocity[0], self.velocity[1])))

        error = planet.radius + 200
        if distance <= error:
            self.state = "Orbit"
            self.orbitAngle2 = -angle
            self.distance = distance
            

    def stateHandler(self, planet):
        if self.state == "Travel":
            self.goTo(planet)
        elif self.state == "Orbit":
            self.circle(planet)

    def update(self, g_loc):
        self.x += self.velocity[0]
        self.y += self.velocity[1]


        cfunc.blitRotate(self, g_loc)
        self.center = [self.rect.x + self.center_x, self.rect.y + self.center_y]
        self.pos = self.center

    def lineOfSight(self):#Need a robust collision/search method for AI to function
        pass
        

    def shoot(self, projectile_list):
        projectile_list.add(Bullet(self.x - g_locx, self.y + g_locy, "Enemy", 10, self.angle, 20))#Change the sel.x and .y to match gun hole ports



