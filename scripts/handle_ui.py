import pygame, sys

def handle_ui(pos, state, button_list, player, slider_list = []):
    for slider in slider_list:
       slider.is_over(pos, state)

    for button in button_list:
        is_over, is_clicked = button.check_mouse(pos, state)
        if is_over:
            if is_clicked:
                player.game_state = button.state
            return True

    return False
        #return is only used for projectiles

    