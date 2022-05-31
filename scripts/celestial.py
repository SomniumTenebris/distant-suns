import pygame
import math
import core_functions as cfunc
import global_vars as gbv


####################
# Celestial Bodies #
####################

class Celestial(pygame.sprite.Sprite):
    def __init__(self, x, y, name, mass, scale, image, radius):
        pygame.sprite.Sprite.__init__(self)
        
        self.mass = mass
        self.radius = radius

        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, scale)

        self.image_thumbnail = pygame.transform.rotozoom(self.image, 0, 0.35)
        # Small sidebar image for display in missions and in the chart

        self.angle = 0
        
        self.mask = pygame.mask.from_surface(self.image)

        self.name = name
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        self.center_x = self.rect[2]/2#These are the centers for the rects, not the actual blitted sprite
        self.center_y = self.rect[3]/2

        self.center = [self.x + self.center_x, self.y + self.center_y]
        self.pos = self.center

        self.rect.x = self.x #- g_locx# + self.center_x
        self.rect.y = self.y #+ g_locy# + self.center_y

        #----- Map Render Attributes -----#
        self.font_color = (10, 30, 40)
        self.name_render = gbv.font.render(str(name), True, (self.font_color))
        self.desc = "A wild and &barren land"
        self.desc_render = cfunc.wrap_text(self.desc, self.font_color)


    def gravity(self, entity):#Planets pull asteroids, enemies, and the player
        G = 30
        distance = math.sqrt((self.center[0]-entity.x)**2 + (self.center[1]-entity.y)**2)#change to center eventually
        entityACCEL = (G*self.mass)/(distance**2)#gives planet's gravitational pull on the object
        
        dx, dy, distance, angle = cfunc.trig2((entity.x, entity.y), self.center)
        
        return entityACCEL, angle

    #########################
    # Map-Related Functions #
    #########################

    def sidebar_info(self, chart):
        gbv.screen.blit(self.name_render, chart.name_pos)
        gbv.screen.blit(self.image_thumbnail, chart.planet_pos)

        for index, line in enumerate(self.desc_render):
            gbv.screen.blit(line, (chart.description_pos[0], chart.description_pos[1] + index*22))


    def map_update(self, chart):#Be sure to reset values after map monkeying
        self.tiny = pygame.transform.rotozoom(self.image, 0, .6/chart.zoom)
        self.tiny_rect = self.tiny.get_rect() #For integration, use self.map_rect to avoid weird stuff

        self.tiny_center_x = self.tiny_rect[2]/2#These are the centers for the rects, not the actual blitted sprite
        self.tiny_center_y = self.tiny_rect[3]/2
        self.map_radius = self.radius / chart.zoom

        self.chart_pos = [(self.x + chart.global_coords[0])/chart.zoom + chart.offset[0],
                    (self.y + chart.global_coords[1])/chart.zoom + chart.offset[0]]#Update tiny planet pos

class Planet(Celestial):#Eventually add second non-colllidable layer
    def __init__(self, x, y, name, mass, scale, image, radius):
        Celestial.__init__(self, x, y, name, mass, scale, image, radius)
        
        self.velocity = [0, 0]
        self.landedAngle = 0
        
        self.halo = pygame.image.load("result.png").convert_alpha()
        self.halo = pygame.transform.rotozoom(self.halo, 0, .8)

        self.halo_rect = self.halo.get_rect()

        ###########
        # Physics #
        ###########

        self.ANGULARSPEED = 0.00

 
    def update(self, g_loc):
        g_locx, g_locy = g_loc

        self.center = [self.x - g_locx, self.y + g_locy]
        self.pos = self.center

        self.rect.x = self.x - g_locx
        self.rect.y = self.y + g_locy

        gbv.screen.blit(self.halo, (self.rect.x - self.halo_rect[2]/2, self.rect.y- self.halo_rect[3]/2))

        self.angle += self.ANGULARSPEED
        if self.angle > 360:
            self.angle -= 360

        cfunc.blitRotate(self, g_loc)


        
        #pygame.draw.circle(gbv.screen, (0,0,68), (self.pos[0], self.pos[1]), 15)
        #pygame.draw.circle(gbv.screen, (0,255,0), (self.center[0], self.center[1]), 5)

class BlackHole(Celestial):#Eventually add second non-colllidable layer
    def __init__(self, x, y, name, mass, radius):
        self.image = pygame.image.load("Star.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 1)
        scale = 1

        Celestial.__init__(self, x, y, name, mass, scale, self.image, radius)
        
        ###########
        # Physics #
        ###########

        self.ANGULARSPEED = .2

    def update(self, g_loc):
        g_locx, g_locy = g_loc
        
        self.center = [self.x - g_locx + self.center_x, self.y + g_locy + self.center_y]
        self.pos = self.center

        self.rect.x, self.rect.y = self.x - g_locx, self.y + g_locy

        gbv.screen.blit(self.image, (self.x - g_locx, self.y + g_locy))

class Moon(Celestial):
    def __init__(self, x, y, name, mass, scale, image, radius, parent):
        Celestial.__init__(self, x, y, name, mass, scale, image, radius)
        
        self.velocity = [0, 0]
        self.landedAngle = 0

        self.parent = parent
        dx, dy, distance, angle = cfunc.trig2(self.pos, self.parent.pos)#trig2((self.x, self.y), (self.parent.x, self.parent.y))
        self.orbit_angle = angle
        self.distance = distance #Or manually set

        ###########
        # Physics #
        ###########

        self.ANGULARSPEED = 0.001

    def orbit(self):
        self.orbit_angle += self.ANGULARSPEED
        self.velocity[0] = (self.distance) * math.sin(self.angle) * self.ANGULARSPEED
        self.velocity[1] = (self.distance) * math.cos(self.angle) * self.ANGULARSPEED
        self.x += self.velocity[0]
        self.y += self.velocity[1]

 
    def update(self, g_loc):
        self.orbit()
        g_locx, g_locy = g_loc

        self.center = [self.x - g_locx, self.y + g_locy]
        self.pos = self.center

        self.rect.x = self.x - g_locx
        self.rect.y = self.y + g_locy

        self.angle += self.ANGULARSPEED
        if self.angle > 360:
            self.angle -= 360

        cfunc.blitRotate(self, g_loc)
        #pygame.draw.circle(gbv.screen, (0,0,68), (self.pos[0], self.pos[1]), 15)
        #pygame.draw.circle(gbv.screen, (0,255,0), (self.center[0], self.center[1]), 5)


class Star(Celestial):#Should the star deal heat damage? I don't sure yet
    def __init__(self, x, y, name, mass, scale, image, radius):
        Celestial.__init__(self, x, y, name, mass, scale, image, radius)


        ###########
        # Physics #
        ###########
        self.ANGULARSPEED = .2

    def update(self, g_loc):
        g_locx, g_locy = g_loc

        self.center = [self.x - g_locx + self.center_x, self.y + g_locy + self.center_y]
        self.pos = self.center

        self.rect.x, self.rect.y = self.x - g_locx, self.y + g_locy
        gbv.screen.blit(self.image, (self.x - g_locx, self.y + g_locy))

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity, size):
        pygame.sprite.Sprite.__init__(self)

        if size == "Small":
            self.mass = 100
            self.image = pygame.image.load("data/images/celestial/Asteroid3.png").convert_alpha()
            self.radius = 50
            self.health = 500

        elif size == "Medium":
            self.mass = 700
            self.image = pygame.image.load("data/images/celestial/Asteroid2.png").convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, 1.2)
            self.radius = 100
            self.health = 2000

        elif size == "Large":
            self.mass = 2000
            self.image = pygame.image.load("data/images/celestial/Asteroid1.png").convert_alpha()
            self.radius = 200
            self.health = 4000


        self.sizes = ["Small", "Medium", "Large"]
        self.size = size

        self.rect = self.image.get_rect()
        self.center_x = self.rect[2]/2#These are the centers for the rects, not the actual blitted sprite
        self.center_y = self.rect[3]/2

        self.x = x
        self.y = y
        self.angle = 0
        self.pos = [x, y]
        
        self.velocity = velocity

        self.collisionCounter = 0

        self.ANGULARSPEED = 0.1

    def split(self):

        explosion = Explosion((self.pos), 2) 
        explosionList.append(explosion)#When explosion animation stops, the player dies. Big sad

        if self.size == "Small":
            asteroidList.remove(self)


        elif self.size == "Medium" or self.size == "Large":
            magnitude = 1
            space = 100
            angle = math.radians(self.angle)

            p1 = [self.x + math.cos(angle) * space, self.y + math.sin(angle) * space]
            p2 = [self.x - math.cos(angle) * space, self.y - math.sin(angle) * space]
            #p1 = [self.pos[0] + math.cos(angle) * space, self.pos[1] + math.sin(angle) * space]
            #p2 = [self.pos[0] - math.cos(angle) * space, self.pos[1] - math.sin(angle) * space]
            v1 = [math.cos(angle) * magnitude, math.sin(angle) * magnitude]
            v2 = [-math.cos(angle) * magnitude, -math.sin(angle) * magnitude]

            index = self.sizes.index(self.size)
            size = self.sizes[index - 1]
            asteroidList.remove(self)
            asteroidList.add(Asteroid(p1[0], p1[1], v1, size))
            asteroidList.add(Asteroid(p2[0], p2[1], v2, size))

        del self

    def update(self, g_loc):
        g_locx, g_locy = g_loc

        self.angle += self.ANGULARSPEED
        self.y += self.velocity[1]
        self.x += self.velocity[0]

        self.pos = [self.x - g_locx, self.y + g_locy]
        cfunc.blitRotate(self, g_loc)

        #pygame.draw.circle(gbv.screen, (255,255,0), (self.pos), 10)
