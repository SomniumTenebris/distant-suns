import pygame, sys
import random, math
from time import sleep

#import scripts.global_vars as gbv




gbv.screen = screen

import scripts.spaceships as ship_file
import scripts.player as player_file

#----- Devlog -----#
# 3/1/2022 - Made new file for prettiness, finished pathinding algorithm mostly, moving onto mission system design

#----- End Devlog -----#

global held_down, thrust, landed, masterCollide, projectileList, g_locx, g_locy, dg_locx, dg_locy, player, enemy_list, explosionList #Delete masterCollide once system is centralized

pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])

font = pygame.font.SysFont('ErasITC', 25)
g_locx = g_locy = dg_locx = dg_locy = 0


landed = False

                ############################
################# Main Objects and Sprites ######################
                ############################
        
##################
# Sector Creator #
##################

class Sector():
    def __init__(self, name, planets): #Eventully, this will include boundries and other information
        self.planets = planets
        self.name = name

#######################
# Planet Sector Lists #
#######################

#################
# Quest Handler #
#################

class Quest():#Quest Handler for player. The Player sprite deals with the physical player, while this deals with the player's quests
    def __init__(self):
        self.quests = []
        self.pending = []
        self.completed = []

        #self.enemy_list = enemy_list
        
        pass
    def complete():
        pass

    def begin(self):
        global enemy_list
        '''box = dialogueBox("""Name, we are recieving an &incoming transmission from &the Lazax.""", "Nekro.png")#Ampresands are the equivalent of line breaks
        dialogueBox.wait()
        box = dialogueBox("""Your presence is requested &immediately. """, "Lazax.png")
        dialogueBox.wait()
        box = dialogueBox("""Uploading coordinates to &the rendevous now.&Get here as quickly &as you can. """, "Lazax.png")
        dialogueBox.wait()'''
        #This will cause the map to flash, with a new point set on there
        
        #enemy1 = Enemy(0, 0, 0, 0)
        enemy = Enemy(000, -200, "Approach")

        enemy_list = pygame.sprite.Group(enemy)
        #print(enemy_list)

        self.quests.append("Go to the rendevous point")

class Mission():
    def __init__(self):
        self.completed = False
        self.condition = "player.planet.name == 'Abyz'"

    def check_condition(self, player):
        try:
            check = eval(self.condition)
        except:
            pass
        else:
            if check:
                print("Yahoo!")
        

    

################################
# Bullets and Auto-Projectiles #
################################

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, origin, speed, angle, damage):#Origin is who shot the bullet
        pygame.sprite.Sprite.__init__(self)

        self.angle = angle
        
        self.image = pygame.image.load("Bullet.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, self.angle + 90, .5)

        self.rect = self.image.get_rect()
        self.center_x, self.center_y = self.rect[2]/2, self.rect[3]/2


        self.pos = [x, y]#[self.x - self.center_x, self.y - self.center_y]
        self.rect.x, self.rect.y = self.pos[0] - self.center_x, self.pos[1] - self.center_y

        self.speed = speed
        self.life = 300

        self.velocity = [-self.speed*math.sin(math.radians(self.angle)), -self.speed*math.cos(math.radians(self.angle))]

        self.radius = 5
        self.mass = 5

        self.origin = origin
        self.damage = damage

    def update(self):
        
        self.velocity[0] = -self.speed*math.sin(math.radians(self.angle))
        self.velocity[1] = -self.speed*math.cos(math.radians(self.angle))

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.rect.x = self.pos[0] - self.center_x
        self.rect.y = self.pos[1] - self.center_y


        self.life -= 1

        if self.life <= 0:
            self.kill()

####################
# Celestial Bodies #
####################

#NOTE: I should use Python class inheritance to simplify and condense celestial body code

class Celestial(pygame.sprite.Sprite):
    def __init__(self, x, y, name, mass, scale, image, radius):
        pygame.sprite.Sprite.__init__(self)
        
        self.mass = mass
        self.radius = radius

        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, scale)

        self.angle = 0
        
        self.mask = pygame.mask.from_surface(self.image)

        self.name = name
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        self.center_x = self.rect[2]/2#These are the centers for the rects, not the actual blitted sprite
        self.center_y = self.rect[3]/2

        self.center = [self.x - g_locx + self.center_x, self.y + g_locy + self.center_y]
        self.pos = self.center

        self.rect.x = self.x - g_locx# + self.center_x
        self.rect.y = self.y + g_locy# + self.center_y

    def gravity(self, entity):#Planets pull asteroids, enemies, and the player
        G = 30
        distance = math.sqrt((self.center[0]-entity.x)**2 + (self.center[1]-entity.y)**2)#change to center eventually
        entityACCEL = (G*self.mass)/(distance**2)#gives planet's gravitational pull on the object
        
        dx, dy, distance, angle = trig2((entity.x, entity.y), self.center)
        
        return entityACCEL, angle

class Planet(Celestial):#Eventually add second non-colllidable layer
    def __init__(self, x, y, name, mass, scale, image, radius):
        Celestial.__init__(self, x, y, name, mass, scale, image, radius)
        
        self.velocity = [0, 0]
        self.landedAngle = 0

        ###########
        # Physics #
        ###########

        self.ANGULARSPEED = 0.01

 
    def update(self):
        self.center = [self.x - g_locx, self.y + g_locy]
        self.pos = self.center

        self.rect.x = self.x - g_locx
        self.rect.y = self.y + g_locy

        self.angle += self.ANGULARSPEED
        if self.angle > 360:
            self.angle -= 360

        blitRotate(self)
        pygame.draw.circle(screen, (0,0,68), (self.pos[0], self.pos[1]), 15)
        pygame.draw.circle(screen, (0,255,0), (self.center[0], self.center[1]), 5)

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

    def update(self):
        self.center = [self.x - g_locx + self.center_x, self.y + g_locy + self.center_y]
        self.pos = self.center

        self.rect.x, self.rect.y = self.x - g_locx, self.y + g_locy

        screen.blit(self.image, (self.x - g_locx, self.y + g_locy))

class Moon(Celestial):
    def __init__(self, x, y, name, mass, scale, image, radius, parent):
        Celestial.__init__(self, x, y, name, mass, scale, image, radius)
        
        self.velocity = [0, 0]
        self.landedAngle = 0

        self.parent = parent
        dx, dy, distance, angle = trig2(self.pos, self.parent.pos)#trig2((self.x, self.y), (self.parent.x, self.parent.y))
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

 
    def update(self):
        self.orbit()
        self.center = [self.x - g_locx, self.y + g_locy]
        self.pos = self.center

        self.rect.x = self.x - g_locx
        self.rect.y = self.y + g_locy

        self.angle += self.ANGULARSPEED
        if self.angle > 360:
            self.angle -= 360

        blitRotate(self)
        pygame.draw.circle(screen, (0,0,68), (self.pos[0], self.pos[1]), 15)
        pygame.draw.circle(screen, (0,255,0), (self.center[0], self.center[1]), 5)


class Star(Celestial):#Should the star deal heat damage? I don't sure yet
    def __init__(self, x, y, name, mass, scale, image, radius):
        Celestial.__init__(self, x, y, name, mass, scale, image, radius)


        ###########
        # Physics #
        ###########
        self.ANGULARSPEED = .2

    def update(self):
        self.center = [self.x - g_locx + self.center_x, self.y + g_locy + self.center_y]
        self.pos = self.center

        self.rect.x, self.rect.y = self.x - g_locx, self.y + g_locy
        screen.blit(self.image, (self.x - g_locx, self.y + g_locy))

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity, size):
        pygame.sprite.Sprite.__init__(self)

        if size == "Small":
            self.mass = 100
            self.image = pygame.image.load("Asteroid3.png").convert_alpha()
            self.radius = 50
            self.health = 500

        elif size == "Medium":
            self.mass = 700
            self.image = pygame.image.load("Asteroid2.png").convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, 1.2)
            self.radius = 100
            self.health = 2000

        elif size == "Large":
            self.mass = 2000
            self.image = pygame.image.load("Asteroid1.png").convert_alpha()
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

    def update(self):
        self.angle += self.ANGULARSPEED
        self.y += self.velocity[1]
        self.x += self.velocity[0]

        self.pos = [self.x - g_locx, self.y + g_locy]
        blitRotate(self)

        pygame.draw.circle(screen, (255,255,0), (self.pos), 10)

############
# Text Box #
############

class dialogueBox(pygame.sprite.Sprite):#Once it's called, it's initiated.
    def __init__(self, text, image):#SET X AND Y BEFOREHAND
        pygame.sprite.Sprite.__init__(self)

        font = pygame.font.SysFont('ErasITC', 25)


        BG_COLOR = pygame.Color('gray12')
        BLUE = pygame.Color('dodgerblue')
        box = pygame.image.load("TextBox.png").convert_alpha()
        boxRect = box.get_rect()

        textOffset = 0
        hasRendered = []
        TxtWidth = 30 #Distance from edge of text box
        TxtHeight = 70

        box_x = 200
        box_y = 500

        # Triple quoted strings contain newline characters.
        self.text_orig = text

        # Create an iterator so that we can get one character after the other.

        textList = self.text_orig.split("&")

        for i in range(0, len(textList)):
            text_iterator = iter(textList[i])
            text = ''

            done = False
            while not done:
                sleep(.01)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    # Press 'r' to reset the text. Eliminate in actual version
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            text_iterator = iter(self.text_orig)
                            text = ''

                if len(text) < len(textList[i]):
                    text += next(text_iterator)

                else:
                    hasRendered.append(text)
                    done = True



                screen.blit(box, (box_x, box_y))

                Character = pygame.image.load(image)
                screen.blit(Character, (375 + box_x, 50 + box_y))

                for b in range(0, len(hasRendered)):
                    img = font.render(hasRendered[b], True, BLUE)  # Recognizes newline characters.
                    screen.blit(img, (box_x + TxtWidth, box_y + 70 + 30*b))



                

                
                img = font.render(text, True, BLUE)
                screen.blit(img, (box_x + 30, box_y + 70 + 30*i))

                pygame.display.update(projectileList.draw(screen))
                pygame.display.update(masterCollide.draw(screen))
                pygame.display.update(asteroidList.draw(screen))
                player.stop()
                player.update()

                
                pygame.display.flip()
                    
    def wait():#Animate box while waiting
        run = True
        while run:
            
            for event in pygame.event.get():
                key = pygame.key.get_pressed()
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    run = False
            pygame.display.flip()
            
################################
# Camera and Screen Animations #
################################

class Fade(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.display.get_surface().get_rect()
        self.image = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
        self.alpha = 0
        self.direction = 1

    def update(self):
        self.image.fill((0, 0, 0, self.alpha))
        self.alpha += self.direction
        if self.alpha > 255 or self.alpha < 0:
            self.direction *= -1
            self.alpha += self.direction

class Camera():#Handles global variables
    def __init__(self, WIDTH, HEIGHT, g_locx, g_locy):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.error = 10
        self.SPEED = 1

        self.g_loc = [g_locx, g_locy]
       
    def recenter(self, player):
        global g_locx, g_locy
        screenCenter = (WIDTH/2, HEIGHT/2)
        delta_x, delta_y, distance, angle = trig2(screenCenter, player.pos)


        angle = math.degrees(angle)
        angle = bound(angle)
        angle = math.radians(angle)

        if distance >= self.error:
            g_locx += -self.SPEED*math.sin(angle)
            g_locy += self.SPEED*math.cos(angle)

    def update(self, player, g_locx, g_locy):
        if (player.x - g_locx) <= self.WIDTH/4 and player.velocity[0] < 0:
            g_locx += player.velocity[0]
            dg_locx = player.velocity[0]
        if (player.x - g_locx) >= 3*self.WIDTH/4 and player.velocity[0] > 0:
            g_locx += player.velocity[0]
            dg_locx = player.velocity[0]

        else:
            dg_locx = 0
            
        if (player.y + g_locy) <= self.HEIGHT/4 and player.velocity[1] < 0:
            g_locy -= player.velocity[1]
            dg_locy = player.velocity[1]
        if (player.y + g_locy) >= 3*self.HEIGHT/4 and player.velocity[1] > 0:
            g_locy -= player.velocity[1]
            dg_locy = player.velocity[1]
            
        else:
            dg_locy = 0

        self.g_loc = [g_locx, g_locy]
        
        return g_locx, g_locy, dg_locx, dg_locy
    
#####################################
# Animations and Extraneous Visuals #
#####################################

class Explosion():#Eventually add smoke and effects, but good for now.
    def __init__(self, pos, size):
        self.x = pos[0]
        self.y = pos[1]
        self.size = size

        self.duration = 20
        self.type = ""#Type indicates number of circles, color, and more

        self.radius1 = 20 * size
        self.radius2 = 20 * size
        self.radius3 = 20 * size
        self.radius4 = 20 * size


    def update(self):#Fine tune to look nicer
        pygame.draw.circle(screen, (255,0,0), (self.x, self.y), self.radius1)
        self.radius1 += 1.6 * self.size

        self.duration -= 1

        if self.duration <= 15:
            pygame.draw.circle(screen, (255,140, 0), (self.x, self.y), self.radius2)
            self.radius2 += 1.8 * self.size

        if self.duration <= 10:
            pygame.draw.circle(screen, (255,255, 0), (self.x, self.y), self.radius3)
            self.radius3 += 2.2 * self.size

        if self.duration <= 5:
            pygame.draw.circle(screen, (255,255, 255), (self.x, self.y), self.radius4)
            self.radius4 += 2.6 * self.size

        if self.duration <= 0:
            explosionList.remove(self)
            del self

######################
# Homeless Functions #
######################

def trig(entity1, entityx, entityy):#Maybe universalize to not only include objs
    delta_x = entity1.x - entityx
    delta_y = entity1.y - entityy

    distance = math.sqrt((delta_x)**2+(delta_y)**2)
    #print(delta_x, delta_y, distance)

    angle = math.asin(delta_y/distance)#For some reason, Law of Sines is superior to tan
    #angle = math.atan(delta_y/delta_x)#Added pi to compensate for my weird angular system

    return delta_x, delta_y, distance, angle

def velComp(entity, angle):
    vel_x = entity.speed*math.cos(math.radians(angle))
    vel_y = entity.speed*math.sin(math.radians(angle))
    return vel_x, vel_y

def accelComp(entity, angle):
    accel_x = entity.SPEED*math.cos(math.radians(angle))
    accel_y = entity.SPEED*math.sin(math.radians(angle))
    return accel_x, accel_y

def gravity(obj, planet):
    G = 10 #gravitational Constant
    delta_y = (planet.center[1]-obj.pos[1])
    delta_x = (planet.center[0]-obj.pos[0])
    
    distance = math.sqrt(delta_x**2 + delta_y**2)

    gravity = pygame.math.Vector2(delta_x, delta_y).normalize()
    gravity = gravity * G * planet.mass / distance**2#Condense eq?
    
    obj.velocity[0] += gravity.x #Minus because gravity pulls, not pushes
    obj.velocity[1] += gravity.y

def blitRotate(sprite):
    a, b, w, h = sprite.image.get_rect()
    
    sin_a, cos_a = math.sin(math.radians(sprite.angle)), math.cos(math.radians(sprite.angle)) 
    min_x, min_y = min([0, sin_a*h, cos_a*w, sin_a*h + cos_a*w]), max([0, sin_a*w, -cos_a*h, sin_a*w - cos_a*h])

    pivot = pygame.math.Vector2(sprite.center_x, -sprite.center_y)# calculate the translation of the pivot 
    pivot_rotate = pivot.rotate(sprite.angle)
    pivot_move   = pivot_rotate - pivot

    origin = (sprite.x - sprite.center_x + min_x - pivot_move[0] - g_locx, sprite.y - sprite.center_y - min_y + pivot_move[1] + g_locy)#calculate the upper left origin of the rotated image
    
    rotated_image = pygame.transform.rotate(sprite.image, sprite.angle)# get a rotated image

    sprite.rect = rotated_image.get_rect()
    sprite.rect.x += sprite.x - sprite.center_x + min_x - pivot_move[0] - g_locx
    sprite.rect.y += sprite.y - sprite.center_y - min_y + pivot_move[1] + g_locy
    
    screen.blit(rotated_image, origin)

def bounce(entity, entity1):
    ########
    # Note #
    ########
    # When I added mass, the ship sometimes glitches into the various asteroids when stationary. Maybe due to 0-magnitude component vectors? I don't know


    p1, p2 = pygame.math.Vector2(entity.pos[0], entity.pos[1]), pygame.math.Vector2(entity1.pos[0], entity1.pos[1])
    nv1, nv2 = p1 - p2, p2 - p1# Normal, positional vector
    
    v1, v2 = pygame.math.Vector2(entity.velocity[0], entity.velocity[1]), pygame.math.Vector2(entity1.velocity[0], entity1.velocity[1])
    vv1 = v1 - v2# Velocity vector
    vv2 = v2 - v1

    dot1, dot2 = vv1.dot(nv1), vv1.dot(nv2)

    mag = nv1.magnitude_squared() #Should be same for nv1 and nv2

    massRatio = entity.mass/entity1.mass


    vector1 = -dot1/mag * nv1 * massRatio**(-1)
    vector2 = dot2/mag * nv2 * massRatio 

    return vector1, vector2

def bounce2(entity, entity1): # Need to factor in mass
    p1 = pygame.math.Vector2(entity.pos[0], entity.pos[1])
    p2 = pygame.math.Vector2(entity1.pos[0], entity1.pos[1])
    nv1 = p1 - p2# Normal, positional vector
    nv2 = p2 - p1
    
    v1 = pygame.math.Vector2(entity.velocity[0], entity.velocity[1])
    v2 = pygame.math.Vector2(entity1.velocity[0], entity1.velocity[1])
    vv1 = v1 - v2# Velocity vector
    vv2 = v2 - v1

    dot1 = vv1.dot(nv1)
    dot2 = vv1.dot(nv2)#vv1 or vv2? If I have errors, I shuold look here

    mag = nv1.magnitude_squared() #Should be same for nv1 and nv2

    massRatio = entity.mass/entity1.mass

    vector1 = -dot1/mag * nv1 * massRatio**(-1)
    vector2 = dot2/mag * nv2 * massRatio 

    
    return vector1, vector2

def bound(angle):
    if angle < 0:
        angle += 360
    if angle >= 360:
        angle -= 360
    return angle

def angleBound(angle1, angle2, error): #angle1 is the test angle, angle 2 is tested against. Maybe not just angle
    if angle1 + error >= angle2 and angle1 - error <= angle2:
        return True
    else:
        return False

def trig2(point1, point2):#Improved? I think so
    '''def get_type(variable): #Mybe universalization and optimization
        typ = type(variable)
        if typ == list:
            return typ'''
        
    delta_x = point1[0] - point2[0]
    delta_y = point1[1] - point2[1]

    distance = math.sqrt((delta_x)**2+(delta_y)**2)

    angle = math.atan2(delta_x, delta_y)

    if delta_x < 0:
        angle = (math.radians(360) + angle)

    return delta_x, delta_y, distance, angle

def trig3(e1, e2):
    dx = e2.pos[0] - e1.pos[0]
    dy = e2.pos[1] - e1.pos[1]
    angle = math.atan2(dy, dx)
    distance = math.hypot(dx, dy)

    return dx, dy, angle, distance

def scalar_proj(v1, v2): #Where v1 is the object vector and v2 is a position vector
    dot = v1.dot(v2)
    mag = v2.magnitude()
    final = dot/mag
    return final

def vel_update(entity, v): #Where v is a vector
    entity.velocity[0] += v.x
    entity.velocity[1] += v.y


########################################
# Backgrounds and Parallax Experiments #
########################################

class Background():
    def __init__(self):
    
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

        self.x, self.y = 0, 0
    
    def update(self):
        for i in range(0, len(self.stars1)):#Optimize to only draw circles within the view of the screen
            if WIDTH > self.stars1[i][0] - g_locx/100 > 0 and HEIGHT > self.stars1[i][1] - g_locy/100 > 0:
                pygame.draw.circle(screen, (255,255,255), (self.stars1[i][0] - g_locx/100, self.stars1[i][1] + g_locy/100), 3)
        for i in range(0, len(self.stars2)):#Optimize to only draw circles within the view of the screen
            if WIDTH > self.stars2[i][0] - g_locx/100 > 0 and HEIGHT > self.stars2[i][1] - g_locy/100 > 0:
                pygame.draw.circle(screen, (150,175,255), (self.stars2[i][0] - g_locx/300, self.stars2[i][1] + g_locy/300), 2)

#########################
# Miscellaneous Sprites #
#########################

################
# Space Cannon #
################

       
##################################
# End Main Functions and Sprites #
##################################


run = True
thrust = True
collided = False

camera = Camera(WIDTH, HEIGHT, g_locx, g_locy)

gbv.camera = camera

player = player_file.Player(WIDTH/2, HEIGHT/2, 0, 0)
Saudor = Planet(3500, -200, "Saudor", 100, 0.6, "Civilized_Mountains.png", 200)
Abyz = Planet(900, 200, "Abyz", 100, 0.6, "Civilized_Ice.png", 200)

#planet2 = Planet(1000, 300, "Mecatol Rex", 150, 100)

hole1 = Star(2000, 300, "Ion Storm", 450, 2, "Star.png", 225)


#asteroid1 = Asteroid(-100, -100, [1, 1], "Large")
#asteroid2 = Asteroid(400, 400, [0, 0], "Small")


masterCollide = pygame.sprite.Group(Saudor, Abyz)#, planet2)

loadedPlanets = pygame.sprite.Group(Saudor, Abyz)#, planet2)

projectileList = pygame.sprite.Group()
asteroidList = pygame.sprite.Group()#asteroid1, asteroid2)
instaDeathList = pygame.sprite.Group(hole1) #Incudes stars and black holes
explosionList = []

player_list = pygame.sprite.Group()
player_list.add(player)
#compass = Compass(Abyz)

#Cannon = SpaceCannon(200, 200)
cannon_list = pygame.sprite.Group()
#cannon_list.add(Cannon)

enemy_list = pygame.sprite.Group() #Scale up enemies
#enemy_list.add(enemy)#, enemy2)# -- Sets EnemyList to null to avoid lag


fade = pygame.sprite.Group(Fade())

background = Background()

quest = Quest()

mission = Mission()

#gbv.initialize(screen, font, camera, g_locx, g_locy)



#pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP]) - L8r optimization thing


#---------------- Main Loop ----------------------------#
while run:
    
    clock.tick(60)
    screen.fill([10, 0, 30])
    background.update()

################
# Player Input #
################

    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        state = pygame.mouse.get_pressed()
        
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:#and thrust == True:
                held_down_UP = True
                if thrust == True:
                    
                    player.thrust()
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                held_down_LEFT = True

            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                held_down_RIGHT = True
                
            else:
                pass
            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:          
                held_down_UP = False

            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                held_down_LEFT = False

            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                held_down_RIGHT = False

        if event.type == pygame.MOUSEMOTION:#Delete if not using
            pos = pygame.mouse.get_pos()

        if state[0] == True:
            for projectile in player.shoot():
                projectileList.add(projectile)

        if state[1] == True:
            quest.begin()
            print(enemy_list)

        if state[2] == True:
            player.warpDrive()

##########################
# Update Player Movement #
##########################

    if gbv.held_down_UP == True: #Eventually add deceleration
        player.thrust()
    if gbv.held_down_LEFT == True:
        player.turn(1)
    if gbv.held_down_RIGHT == True:
        player.turn(-1)

###########
# Gravity #
###########

    if player.landed == False:
        for i in loadedPlanets:
           player.gravity(i)

    player.gravity(hole1)

#######################
# NPC AI and Behavior #
#######################

########################
# Planetary Collisions #
########################

    collide = pygame.sprite.spritecollide(player, masterCollide, False, pygame.sprite.collide_circle)
    
    if len(collide) > 0:
        collided = True
        player.thrustTimer = 10
        player.planetCollide(collide[0])#MAKE SURE ONLY ONE PLANET AT A TIME
        player.hasCollided = True
        if player.landed == False:#If you hit a planet while not landed, you cannot thrust
            thrust = False
    elif len(collide) <= 0:
        player.hasCollided = False
        player.landed = False
        collided = False
        player.thrustTimer -= 1
        if player.thrustTimer == 0:
            thrust = True

####################
# Updating Sprites #
####################

    for i in explosionList: #Maybe render under planets
        i.update()

    for i in masterCollide: 
        i.update()

    for i in player_list:
        print("From parent class: " + str(gbv.screen))
        i.update()

    for i in enemy_list:
        i.stateHandler(Abyz)
        i.update()

    for i in projectileList:#Optimize later
        i.update()

    for i in cannon_list: #Change to hit target later
        pass
    

    
    g_locx, g_locy, dg_locx, dg_locy = camera.update(player, g_locx, g_locy) #Update camera and global coordinates

##############
# Collisions #
##############


    #If a bullet collides with the player 
    collide = pygame.sprite.spritecollide(player, projectileList, False, pygame.sprite.collide_circle)
    for i in collide:
        if i.origin != "Player":#fix l8r
            player.health -= i.damage
            projectileList.remove(i)
            del i

            
    for a in projectileList:
        collide = pygame.sprite.spritecollide(a, masterCollide, False, pygame.sprite.collide_circle)#Change to rendered on screen
        if len(collide) > 0:
            projectileList.remove(a)

            del a
            print("Splash!")

    for a in enemy_list:
        collide = pygame.sprite.spritecollide(a, projectileList, False, pygame.sprite.collide_circle)
        for i in collide:
            if i.origin != "Enemy":#fix l8r, 
                a.health -= i.damage
                projectileList.remove(i)
                del i

    for i in asteroidList:
        i.update()
        collide = pygame.sprite.spritecollide(i, asteroidList, False, pygame.sprite.collide_circle)
        collide.remove(i)

        for a in collide:
            print(i.velocity)
            j, k = bounce(i, a)
            vel_update(i, j)
            vel_update(a, k)
            print(i.velocity)

        collide = pygame.sprite.spritecollide(i, player_list, False, pygame.sprite.collide_circle)

        for a in collide:
            j, k = bounce(i, a)
            vel_update(i, j)
            vel_update(player, k)
            player.damage(i)

        collide = pygame.sprite.spritecollide(i, projectileList, False, pygame.sprite.collide_circle)
        for a in collide:
            j, k = bounce(i, a)
            vel_update(i, j)
            i.health -= a.damage
            projectileList.remove(a)
            del a


        collide = pygame.sprite.spritecollide(i, masterCollide, False, pygame.sprite.collide_circle)
        for a in collide:
            asteroidList.remove(i)
            del i
            
    collide = pygame.sprite.spritecollide(player, instaDeathList, False, pygame.sprite.collide_circle)
    if len(collide) > 0:
        player.health = 0
            
    for i in cannon_list:
        i.update()
        i.cannon.moveTo(player)
        collide = pygame.sprite.spritecollide(i, projectileList, False, pygame.sprite.collide_circle)
        for a in collide:
            print("HIT")
            i.health -= a.damage
            projectileList.remove(a)
            del a

    hole1.update()

#######################################
# Cleanup, Deletion, and Optimization #
#######################################

    if player.health <= 0 and player.alive == True:
        player.alive = False
        explosion = Explosion(player.pos, 2) 
        explosionList.append(explosion)#When explosion animation stops, the player dies. Big sad
        player_list.remove(player)
        
    for i in enemy_list:
        if i.health <= 0:
            enemy_list.remove(i)
            explosionList.append(Explosion((i.pos), 2))
            del i

    for i in asteroidList:
        if i.health <= 0:
            i.split()
            del i

    for i in cannon_list:
        if i.health <= 0:
            cannon_list.remove(i)
            explosionList.append(Explosion((i.pos), 2))
            del i


    mission.check_condition(player)


###########################
# Temporary Text Blitting #
###########################



    Land = font.render("Landed: " + str(player.landed), True, (0,255,0))
    screen.blit(Land, (0,0))

    Speed = font.render("Speed: " + str(player.speed), True, (0,255,0))
    screen.blit(Speed, (0,30))

    FPS = font.render("Collided: " + str(player.hasCollided), True, (0,255,0))
    screen.blit(FPS, (0,60))

    State = font.render("Thrust: " + str(thrust), True, (0,255,0))
    screen.blit(State, (0,90))

    Angle = font.render("Ship Angle: " + str(player.angle), True, (0,255,0))
    screen.blit(Angle, (0,120))

    pygame.display.update(projectileList.draw(screen))
    player.HUD.update(player)

    pygame.display.flip()
