import pygame, sys
import math
from time import sleep

import scripts.global_vars as gbv
import scripts.player as player_file
import scripts.non_player_ships as nps_file
import scripts.core_functions as cfunc
import scripts.assets as assets
import scripts.celestial as celeste
import scripts.background as bg
import scripts.effects as effects
import scripts.sector_loader as sector_load

#----- Devlog -----#
# 3/1/2022 - Made new file for prettiness, finished pathinding algorithm mostly, moving onto mission system design
# 3/4/2022 - I finished a good portion of the organization and file errors. GBV holds screen & font data, updating requires passing camera info.
#            I also got JSON sector loading working, important to know currentdirectories
# 3/5/22 - I cleaned up the rotation stuff, but that causes a bit of lag. Maybe I need to clean up blitRotate to a simpler formula. Also
#          I worked on particles. I do need to fix rotations though ... look into HDF5
# 3/7/22 - Added planet halos, looking crisp.
#----- End Devlog -----#
#
#----- TODO -----#
# State handler/Machine
# Player-planet collisions are rough when crashing and turning

pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = gbv.width, gbv.height
screen = gbv.screen

font = pygame.font.SysFont('ErasITC', 25)
g_locx = g_locy = 0

pygame.display.set_caption("Distant Suns")

        
##################
# Sector Creator #
##################

def build_sector(celestials_list, physics_list):
    pass

#################
# Quest Handler #
#################

class Quest():#Quest Handler for player. The Player sprite deals with the physical player, while this deals with the player's quests
    def __init__(self):
        self.quests = []
        self.pending = []
        self.completed = []
        #self.enemy_list = enemy_list
        
    def complete():
        pass

    def begin(self):
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

    def check_condition(self, player): #For performance, only check during certain times (give it quest type, perhaps)
        try:
            check = eval(self.condition)
        except:
            pass
        else:
            if check:
                print("Yahoo!")
        
            
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
        delta_x, delta_y, distance, angle = cfunc.trig2(screenCenter, player.pos)


        angle = math.degrees(angle)
        angle = cfunc.bound(angle)
        angle = math.radians(angle)

        if distance >= self.error:
            g_locx += -self.SPEED*math.sin(angle)
            g_locy += self.SPEED*math.cos(angle)

    def update(self, player, g_locx, g_locy):
        if (player.x - g_locx) <= self.WIDTH/4 and player.velocity[0] < 0:
            g_locx += player.velocity[0]
        if (player.x - g_locx) >= 3*self.WIDTH/4 and player.velocity[0] > 0:
            g_locx += player.velocity[0]

        if (player.y + g_locy) <= self.HEIGHT/4 and player.velocity[1] < 0:
            g_locy -= player.velocity[1]
        if (player.y + g_locy) >= 3*self.HEIGHT/4 and player.velocity[1] > 0:
            g_locy -= player.velocity[1]

        self.g_loc = [g_locx, g_locy]
        
        return g_locx, g_locy

##################################
# End Main Functions and Sprites #
##################################

run = True
thrust = True
collided = False



camera = Camera(WIDTH, HEIGHT, g_locx, g_locy)

player = player_file.Player(WIDTH/2, HEIGHT/2, 0, 0, camera)

Saudor, Abyz = sector_load.load_sector(1)[0]
star = celeste.Star(2400, 500, "Rex", 1000, 1, "Star1.png", 300)
masterCollide = pygame.sprite.Group(Saudor, Abyz)#, planet2)
loadedPlanets = pygame.sprite.Group(Saudor, Abyz)#, planet2)

projectileList = pygame.sprite.Group()
asteroidList = pygame.sprite.Group() #asteroid1, asteroid2)
instaDeathList = pygame.sprite.Group() #Incudes stars and black holes
explosionList = []

cannon = assets.SpaceCannon(3500, -440) 
#cannon = assets.SpaceCannon(-100, 0) 


player_list = pygame.sprite.Group()
player_list.add(player)

#Cannon = SpaceCannon(200, 200)
cannon_list = pygame.sprite.Group()
cannon_list.add(cannon)

enemy = nps_file.Enemy(2000, 100, 0, 0, "20")
enemy_list = pygame.sprite.Group(enemy)

background = bg.Background()

quest = Quest()

mission = Mission()

#pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP]) - L8r optimization thing


#---------------- Main Loop ----------------------------#
while run:
    
    clock.tick(60)
    screen.fill([10, 0, 30])
    background.update(camera.g_loc)

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
                player.held_up = True
                
                if thrust == True:
                    player.thrust()
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.held_left = True

            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.held_right = True
                
            else:
                pass
            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:          
                player.held_up = False

            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.held_left = False

            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.held_right = False

        if event.type == pygame.MOUSEMOTION:#Delete if not using
            pos = pygame.mouse.get_pos()

        if state[0] == True:
            player.shoot(projectileList)

        if state[2] == True:
            player.warpDrive()

##########################
# Update Player Movement #
##########################

    if player.held_up == True: #Eventually add deceleration
        player.thrust()
    if player.held_left == True:
        player.turn(1)
    if player.held_right == True:
        player.turn(-1)

###########
# Gravity #
###########

    if player.landed == False: #Limit radius of influence somehow
        for i in loadedPlanets:
           player.gravity(i)


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
        i.update(explosionList)

    for i in masterCollide:
        i.update(camera.g_loc)

    for i in enemy_list:
        i.stateHandler(Saudor)
        i.update(camera.g_loc)

    for i in projectileList:#Optimize later
        i.update()


    star.update(camera.g_loc)

    
        
    g_locx, g_locy = camera.update(player, g_locx, g_locy) #Update camera and global coordinates

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
            j, k = cfunc.bounce(i, a)
            cfunc.vel_update(i, j)
            cfunc.vel_update(a, k)

        collide = pygame.sprite.spritecollide(i, player_list, False, pygame.sprite.collide_circle)

        for a in collide:
            j, k = cfunc.bounce(i, a)
            cfunc.vel_update(i, j)
            cfunc.vel_update(player, k)
            player.damage(i)

        collide = pygame.sprite.spritecollide(i, projectileList, False, pygame.sprite.collide_circle)
        for a in collide:
            j, k = cfunc.bounce(i, a)
            cfunc.vel_update(i, j)
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
        i.update(camera.g_loc, projectileList)

        if cfunc.trig3(player, i)[3] < 1000:
            i.cannon.moveTo(player)
            
        collide = pygame.sprite.spritecollide(i, projectileList, False, pygame.sprite.collide_circle)
        for a in collide:
            i.health -= a.damage
            projectileList.remove(a)
            del a


    for i in player_list:
        i.update(camera.g_loc, masterCollide)


#######################################
# Cleanup, Deletion, and Optimization #
#######################################

    if player.health <= 0 and player.alive == True:
        player.alive = False
        explosion = effects.Explosion(player.pos, 2) 
        explosionList.append(explosion)#When explosion animation stops, the player dies. Big sad
        player_list.remove(player)
        
    for i in enemy_list:
        if i.health <= 0:
            enemy_list.remove(i)
            explosionList.append(effects.Explosion((i.pos), 2))
            del i

    for i in asteroidList:
        if i.health <= 0:
            i.split()
            del i

    for i in cannon_list:
        if i.health <= 0:
            cannon_list.remove(i)
            explosionList.append(effects.Explosion((i.pos), 2))
            del i

    #mission.check_condition(player)

###########################
# Temporary Text Blitting #
###########################

    '''Land = font.render("Landed: " + str(player.landed), True, (0,255,0))
    screen.blit(Land, (0,0))

    Speed = font.render("Speed: " + str(player.speed), True, (0,255,0))
    screen.blit(Speed, (0,30))

    FPS = font.render("Collided: " + str(player.hasCollided), True, (0,255,0))
    screen.blit(FPS, (0,60))

    State = font.render("Thrust: " + str(thrust), True, (0,255,0))
    screen.blit(State, (0,90))

    Angle = font.render("FPS : " + str(clock.get_fps()), True, (0,255,0))
    screen.blit(Angle, (0,120))'''

    pygame.display.update(projectileList.draw(screen))
    player.HUD.update(player)

    pygame.display.flip()
