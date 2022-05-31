import pygame

import scripts.global_vars as gbv
import scripts.player as player_file
import scripts.non_player_ships as nps_file
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
from scripts.pause import handle_pause
from scripts.sector_map import update_map, Map
from scripts.audio_settings import AudioPopup

##########
# Devlog #
##########
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
# 5/20/22 - Solved pathfinding, NEED to fix pos/rect/x-y system for coordinates
# 5/25/22 - Slogged on pathinding
# 5/26/22 - Worked to incorporate map
#----- End Devlog -----#
#
#----- TODO -----#
# Bullets move with g_loc

pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = gbv.width, gbv.height
screen = gbv.screen

pygame.display.set_caption("Distant Suns")

################
# Load Favicon #
################
icon = pygame.image.load("data/images/misc/favicon.png")
pygame.display.set_icon(icon)

##################################
# End Main Functions and Sprites #
##################################

run = True
font = pygame.font.SysFont('ErasITC', 25)


camera = Camera(WIDTH, HEIGHT, 0, 0)

player = player_file.Player(WIDTH/2, HEIGHT/2, 0, 0, camera)

Saudor, Abyz = sector_load.load_sector(1)[0]
star = celeste.Star(2400, 500, "Rex", 1000, 1, "data/images/celestial/star_yellow.png", 300)
masterCollide = pygame.sprite.Group(Saudor, Abyz)#, planet2) #Maybe store as dict for hashing faster
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

enemy = nps_file.Enemy(1400, 500, 0, 0, "20")
enemy1 = nps_file.Enemy(1600, 500, 0, 0, "20")
enemy2 = nps_file.Enemy(1800, 500, 0, 0, "20")
enemy3 = nps_file.Enemy(1600, 700, 0, 0, "20")
enemy4 = nps_file.Enemy(1800, 900, 0, 0, "20")

enemy_list = pygame.sprite.Group(enemy)#, enemy1, enemy2, enemy3, enemy4)

background = bg.Background()

# Maybe make buttons relative to HEIGHT
pause_button = button.Pause_Button()
map_button = button.Button(1020, 20, 50, 50, (255, 255, 0), (255, 200, 0), "Map", img="data/images/ui_elements/map_icon.png")
audio_button = button.Button(20, 730, 50, 50, (255, 255, 0), (255, 200, 0), "Audio", img="data/images/ui_elements/volume.png")
main_button = button.Button(1100, 20, 50, 50, (255, 255, 0), (255, 200, 0), "Main", img="data/images/ui_elements/return.png")

audio_popup = AudioPopup()

button_list = [pause_button, map_button, audio_button]
# List of buttons to display on main screen

chart = Map(masterCollide)
fader = Fader(1)

#pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP]) - L8r optimization thing

#---------------- Main Loop ----------------------------#
while run:
    clock.tick(60)
    fps = font.render(str(clock.get_fps()), True, (0, 255, 79))
    if player.game_state == "Main":
        handle_events(player, projectileList, camera, button_list)
        handle_collisions(player, projectileList, masterCollide, 
                        asteroidList, cannon_list, player_list, instaDeathList, enemy_list, explosionList)
        update(player, player_list, loadedPlanets, explosionList,
               masterCollide, enemy_list, projectileList,
               camera, cannon_list, asteroidList, screen, 
               background, button_list, fader, chart)

    elif player.game_state == "Map":
        update_map(masterCollide, chart, player, [main_button], handle_ui)
   
    elif player.game_state == "Pause":
        handle_pause(player, button_list, handle_ui)

    elif player.game_state == "Audio":
        audio_popup.update()
        handle_pause(player, audio_popup.buttons, handle_ui, slider_list=audio_popup.sliders)

    #gbv.screen.blit(fps, (10, 10))
    pygame.display.flip()