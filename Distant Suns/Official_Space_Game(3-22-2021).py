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
import scripts.sector_loader as sector_load
import scripts.button as button

from scripts.handle_ui import handle_ui
from scripts.fade_screen import Fader
from scripts.camera import Camera

#----- Could consolidate into game_loop -----#
from scripts.game_loop_events import handle_events
from scripts.collision_handler import handle_collisions
from scripts.game_loop_updater import update


#----- Devlog -----#
# 3/1/2022 - Made new file for prettiness, finished pathinding algorithm mostly, moving onto mission system design
# 3/4/2022 - I finished a good portion of the organization and file errors. GBV holds screen & font data, updating requires passing camera info.
#            I also got JSON sector loading working, important to know currentdirectories
# 3/5/22 - I cleaned up the rotation stuff, but that causes a bit of lag. Maybe I need to clean up blitRotate to a simpler formula. Also
#          I worked on particles. I do need to fix rotations though ... look into HDF5
# 3/7/22 - Added planet halos, looking crisp.
# 3/10/22 - Outsourced/organized a few more items for code organization. Finished basic map prototype. Looking good for Fiverr v2.0
# 3/11/22 - Moved out camera class, cut this file down to 150 lines. Made mission hub, looking pretty good, actually
# 3/21/22 - Worked a touch on state machine, player shoots when you click on button, so not the greatest. Also, no color change on hover is a bit of a problem.
# 3/22/22 - Began to directly incorporate an enemy AI to the game, just semi-intelligent pathfinding and stuff. 
#----- End Devlog -----#
#
#----- TODO -----#
# State handler/Machine

pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = gbv.width, gbv.height
screen = gbv.screen

pygame.display.set_caption("Distant Suns")

##################
# Sector Creator #
##################

def build_sector(celestials_list, physics_list):
    pass

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

##################################
# End Main Functions and Sprites #
##################################

run = True

camera = Camera(WIDTH, HEIGHT, 0, 0)

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
cannon_list = pygame.sprite.Group()
cannon_list.add(cannon)

player_list = pygame.sprite.Group()
player_list.add(player)

enemy = nps_file.Enemy(1500, 800, 0, 0, "20")
enemy_list = pygame.sprite.Group(enemy)

background = bg.Background()

pause_button = button.Button(1100, 20, 50, 50, (255, 255, 0), (255, 200, 0))
button_list = [pause_button]

mission = Mission()

fader = Fader(1)

#pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP]) - L8r optimization thing


#---------------- Main Loop ----------------------------#
while run:
    clock.tick(60)
    if player.game_state == "Main":
        handle_events(player, projectileList, camera, button_list)
        handle_collisions(player, projectileList, masterCollide, asteroidList, cannon_list, player_list, instaDeathList, enemy_list)
        update(player, player_list, loadedPlanets, explosionList,
               masterCollide, enemy_list, projectileList,
               camera, cannon_list, asteroidList, screen, background, button_list, fader)

        
    elif player.game_state == "Pause":
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pos = pygame.mouse.get_pos()
        state = pygame.mouse.get_pressed()
        handle_ui(pos, state, button_list, player)

        for button in button_list:
            button.update()

        player.held_up, player.held_left, player.held_right = False, False, False


    pygame.display.flip()