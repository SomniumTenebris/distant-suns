import pygame, sys

def handle_pause(player, button_list, handle_ui, slider_list = []):
    
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.held_up = True
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.held_left = True
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
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

    pos = pygame.mouse.get_pos()
    state = pygame.mouse.get_pressed()
    handle_ui(pos, state, button_list, player, slider_list)

    for button in button_list:
        button.update()

