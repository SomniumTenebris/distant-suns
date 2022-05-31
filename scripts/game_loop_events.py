import pygame, sys
from handle_ui import handle_ui

#Change thrust to player.thrust without overriding function namespace

def handle_events(player, projectileList, camera, button_list):
    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:#and thrust == True:
                player.held_up = True
                
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.held_left = True

            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.held_right = True

            #----- Testing -----#
            elif event.key == pygame.K_SPACE:
                print("Player Position: ", player.pos)
                print("Camera Position: ", camera.g_loc)

            else:
                pass
            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:          
                player.held_up = False

            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.held_left = False

            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.held_right = False

    pos = pygame.mouse.get_pos()
    state = pygame.mouse.get_pressed()
    
    over_button = handle_ui(pos, state, button_list, player)

    if state[0] == True and over_button == False and player.alive == True: #Don't shoot if the player is over a button
        player.shoot(projectileList)

    if state[2] == True:
        player.warpDrive(camera.g_loc)

##########################
# Update Player Movement #
##########################

    if player.held_up == True: #Eventually add deceleration
        player.thrust()
    if player.held_left == True:
        player.turn(1)
    if player.held_right == True:
        player.turn(-1)
    
