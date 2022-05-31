import pygame
import math

import core_functions as cfunc
from spaceships import Spaceship
from projectiles import Bullet
import global_vars as gbv
import effects as eff

class Player(Spaceship): #Maybe class inheritance could be used to simplify spaceship code across player and enemies
    def __init__(self, x, y, angle, speed, camera):
        
        self.image = pygame.image.load("data/images/ships/Ship.png").convert_alpha()
        #self.image = pygame.image.load("result.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, .25)

        self.camera = camera

        Spaceship.__init__(self, x, y, angle, speed)

        self.radius = 30
        self.landed = False
        self.planet = None
        self.landed_timer_MAX = 12
        self.landed_timer = self.landed_timer_MAX
        #self.thrust = True

        self.game_state = "Main"
        
        #self.collisionCounter = 0
        self.HUD = HUD(self)


        self.particles = []
        self.hyper_lines = []

        #----- Gun ports 
        self.portA = [self.pos[0] + math.cos(angle)*self.SPACE, self.pos[1] + math.sin(angle)*self.SPACE]
        self.portB = [self.pos[0] - math.cos(angle)*self.SPACE, self.pos[1] - math.sin(angle)*self.SPACE]

        self.shoot_cooldown = 0
        self.shoot_cooldown_MAX = 10

        #-------- Physics -----------#
        self.MAXSPEED = .05
        self.CRUISESPEED = .02
        self.ACCEL = .05
        self.ANGULARSPEED = 3
        self.mass = 100
        
        self.maxSpeed = 5
        self.harmSpeed = 3 #Speed of harm from planetary collisions

        #----- User Inputs -----#
        self.held_up = False
        self.held_left = False
        self.held_right = False

    def thrust(self):
        if self.speed <= self.MAXSPEED:#Some sort of normalization, accel
            self.speed += self.ACCEL
        else:
            self.speed = self.MAXSPEED#Not sure if necessary

        vector = [self.speed*-math.sin(math.radians(self.angle)), self.speed*-math.cos(math.radians(self.angle))]
        self.velocity = [a + b for a, b in zip(vector, self.velocity)]

        self.particles.append(eff.Particle(self.pos, self.angle, [5, 16], [-6, 6], [4, 20]))

    def turn(self, direction): #direction is -1 or 1
        if self.landed == False:
            self.angle = cfunc.bound(self.angle + self.ANGULARSPEED * direction) # 'bound' keeps the ships's angle between 0 and 360

        if direction == -1:
            self.particles.append(eff.Particle(self.portA, self.angle, [5, 8], [0, 0], [4, 10], decay = 0.25))
        else:
            self.particles.append(eff.Particle(self.portB, self.angle, [5, 8], [0, 0], [4, 10], decay = 0.25))


    def warpDrive(self, g_loc):
        if self.WarpCooldown <= 0:
            self.warpCounter = 10

            self.preSpeed = self.speed
         
            self.speed = 35
            self.WarpCooldown = 100

            vector = [self.speed*-math.sin(math.radians(self.angle)), self.speed*-math.cos(math.radians(self.angle))]
            self.velocity = [a + b for a, b in zip(vector, self.velocity)]

            self.preWarpVelocity = [self.preSpeed*-math.sin(math.radians(self.angle)), self.preSpeed*-math.cos(math.radians(self.angle))]

            for i in range(10):
                self.hyper_lines.append(eff.Hyper_Line(self.portB, self.angle, g_loc))
        else:
            pass
        
    def match(self, planet): #Maybe gravity is throwing it all off.
        self.angle += planet.ANGULARSPEED
        self.velocity[0] = (planet.radius) * math.sin(self.angle) * planet.ANGULARSPEED
        self.velocity[1] = (planet.radius) * math.cos(self.angle) * planet.ANGULARSPEED
        #self.landed = True

    def parent_to_planet(self, planet):
        pass

    def moveTo(self, point):#Call during each game loop, cutscenes and whatnot
        delta_x, delta_y, distance, angle = cfunc.trig2(self.pos, point)
        angle = math.degrees(angle)
        angle = cfunc.bound(angle)

        self.approachTurn(angle)
        angle = math.radians(angle)

        self.delta_x, self.delta_y = -self.speed*math.sin(angle), -self.speed*math.cos(angle)

        error = 10
        if distance < error:
            self.delta_x, self.delta_y = 0, 0
            self.reached = True
        else:
            self.reached = False

    def orbit(self, planet):
        distance = 0 #Distance above planet at which ship orbits
        k = distance + planet.radius
    
        if self.orbitAngle > 360:
            self.orbitAngle -= 360
        
        angle = math.radians(self.orbitAngle)
        change = 0.2 #Angular velocity, base on radius and max speed of enemy

        pos = (planet.pos[0] - math.sin(angle)*k, planet.pos[1] - math.cos(angle)*k)
        #pygame.draw.circle(screen, (255,0,0), (pos), 5)

        self.moveTo(pos)
        self.orbitAngle += change

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

    def calculatePorts(self):
        angle = math.radians(180) - math.radians(self.angle)

        self.portA = [self.pos[0] + math.cos(angle)*self.SPACE, self.pos[1] + math.sin(angle)*self.SPACE]
        self.portB = [self.pos[0] - math.cos(angle)*self.SPACE, self.pos[1] - math.sin(angle)*self.SPACE]
    
    def stop(self):
        self.velocity[0] = 0
        self.velocity[1] = 0
        
    def gravity(self, planet):
        cfunc.gravity(self, planet)
       
    def planetCollide(self, planet):
        error = 15
        delta_y = (planet.center[1]-self.pos[1])
        delta_x = (planet.center[0]-self.pos[0])

        distance = math.hypot(delta_x, delta_y)
        angle = math.atan2(delta_y, delta_x)

        hypotenuse = math.hypot(self.velocity[0], self.velocity[1])#Added
        shipAngle = math.atan2(self.velocity[1], self.velocity[0])#Add

        tangent = math.atan2(delta_y, delta_x)

        test_angle = cfunc.bound(90 - math.degrees(angle)) #Gets angle within 0 to 360

        if cfunc.angleBound(self.angle, test_angle, error):#no landing inside a planet
            self.land(planet)
            self.camera.recenter(self)
            
            if self.landed == False: #Fix error when ship flies to planet, but is accelerating away from planet
                self.orbitAngle = angle #Angle of ship to planet
                
            elif self.speed > self.harmSpeed: #Change from hardcode to something else
                speed = pygame.math.Vector2(self.velocity[0], self.velocity[1]) #Well, I need to change this to the ship's velocity towards the planet
                pos =  pygame.math.Vector2(planet.x - self.x, planet.y - self.y)
                force = cfunc.scalar_proj(speed, pos)
                self.health -= 15*force

            self.landed = True

        elif self.landed == False and self.hasCollided == False:
            v1, v2 = cfunc.bounce(self, planet) #Maybe implement a minimum bounce
            vel = v1

            min_vel = 2
            if v1.magnitude() < min_vel:
                vel = v1.normalize()*min_vel

            velocity = pygame.math.Vector2(v1.x, v1.y) #Well, I need to change this to the ship's velocity towards the planet
            self.velocity[0], self.velocity[1] = vel.x, vel.y

            pos =  pygame.math.Vector2(planet.x - self.x, planet.y - self.y)
            force = cfunc.scalar_proj(velocity, pos)
            self.health -= -15*force #Some damage constant?
            self.hasCollided = True
    
    def land(self, planet):#Fix weird global stuff later
        #if self.landed_timer > 0:
            #self.landed_timer -= 1
            
        if self.held_up == False:
            self.landed = True
            self.planet = planet
            self.landed_timer = self.landed_timer_MAX

            self.stop()
                        
        elif self.held_up == True:
            if self.landed == True:# and self.hasCollided == False:
                self.landed = False
                self.planet = None
            elif self.landed == False:
                self.landed = True
                self.planet = planet
                self.stop()

    def damage(self, entity): #Deals with physical collision damage
        velocity = pygame.math.Vector2(self.velocity[0], self.velocity[1]) #Well, I need to change this to the ship's velocity towards the planet
        pos =  pygame.math.Vector2(entity.x - self.x, entity.y - self.y) #Check and fix up coordinate systems
        force = cfunc.scalar_proj(velocity, pos)
        self.health -= -force

    def shoot(self, projectile_list, g_loc):
        if self.shoot_cooldown <= 0:
            projectile_list.add(Bullet(self.portA[0], self.portA[1], "Player", 10, self.angle, 20, g_loc))
            projectile_list.add(Bullet(self.portB[0], self.portB[1], "Player", 10, self.angle, 20, g_loc))
            self.shoot_cooldown = self.shoot_cooldown_MAX

    def handle_particles(self, planets_list, g_loc):
        to_remove = []
        for index, i in enumerate(self.particles):
            if i.radius <= 0:
                to_remove.append(i)
            else:
                for circle in planets_list:
                    if cfunc.trig3(i, circle)[3] < circle.radius:
                        i.bounce()
                i.update()

        for i in to_remove:
            self.particles.remove(i)
            del i

        '''to_remove = []
        for index, i in enumerate(self.hyper_lines):
            i.duration -= 1
            if i.duration <= 0:
                to_remove.append(i)
            else:
                i.update(g_loc)

        for i in to_remove:
            self.hyper_lines.remove(i)
            del i'''


    def update(self, g_loc, planets_list):

        angle = math.radians(180) - math.radians(self.angle)

        self.calculatePorts()

        self.speed = math.hypot(self.velocity[0], self.velocity[1])
        if self.speed > self.maxSpeed:#This alone does not cap the speed. I need to alter the xy velocities manually
            self.speed = self.maxSpeed

        #----- Cooldowns -----#
        if self.warpCounter > 1:
            self.warpCounter -= 1
            self.speed = 35

        if self.warpCounter == 1:
            self.speed = self.preSpeed
            self.warpCounter = 0
            self.WarpCooldown = 100
        
        if self.WarpCooldown > 0:
            self.WarpCooldown -= 1

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


        if self.landed == False and self.velocity != [0, 0]:
            self.velocity = pygame.math.Vector2(self.velocity[0], self.velocity[1]).normalize()*self.speed
        
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
        self.handle_particles(planets_list, g_loc)


        self.pos = [self.x - g_loc[0], self.y + g_loc[1]]

        cfunc.blitRotate(self, g_loc)


        #pygame.draw.circle(gbv.screen, (0,0,150), (self.pos), 5)
        #camera.recenter(self)


class HUD(pygame.sprite.Sprite):#All 3? Or just 1? Is it a sprite? I think playerclass will handle this, then HUD updates with that info
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("data/images/player_assets/HUD.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 180, .3)


        self.rect = self.image.get_rect()
        self.x = 910
        self.y = 70

        self.offset_x = 24
        self.offset_y = 25

        self.width = 160
        self.height = 25
        self.health = player.health
        self.maxhealth = player.maxhealth


    def update(self, player):
        gbv.screen.blit(self.image, (self.x, self.y))

        
        self.health = player.health
        self.maxhealth = player.maxhealth
        pygame.draw.rect(gbv.screen, (0, 255, 25), (self.x + self.offset_x, self.y + self.offset_y, self.width*self.health/self.maxhealth, self.height))

class Compass(pygame.sprite.Sprite): #Is this a sprite? This is likely solely going to be a triangular indicator
    def __init__(self, target): #Target must be given as pos or else normalize this expression
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("planet.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 180, .3)

        self.rect = self.image.get_rect()
        self.x = 600
        self.y = 300
        self.pos = (self.x, self.y)
        self.origin = self.pos
        self.target = target
        self.angle = 0

        self.offset_x = 24
        self.offset_y = 25

        self.width = 160
        self.height = 25
        
    def update(self, player):
        #dx, dy, distance, self.angle = trig2(self.target.pos, player.pos)
        #self.x = 4
        image = pygame.transform.rotozoom(self.image, self.angle, 0)
        gbv.screen.blit(image, self.pos)

