import pygame
import global_vars as gbv

class Button():
    # Parent class, each button will do something different
    def __init__(self, x, y, width, height, color1, color2, state=None, img=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color1
        self.color1 = color1
        self.color2 = color2

        self.state = state

        self.image = None
        if img != None:
            self.image = pygame.image.load(img).convert_alpha()

        self.is_over = False
        self.pressed = False
        self.released = False #Checks to see if the player's released the mouse

    def check_mouse(self, pos, state):
        #Given the position (pos) of the mouse and whether it's been clicked, determines if button has been pressed
        # Returns is_over, is_clicked
        if self.rect.collidepoint(pos):            
            self.is_over = True
            self.color = self.color2
            
            if state[0] and self.released:
                self.pressed = True
                self.released = False
                return True, True
            
            elif not state[0]:
                self.pressed = False
                self.released = True

            return True, False
        
        else:
            self.is_over = False
            self.color = self.color1

            self.released = False
            return False, False

    def check_mouse(self, pos, state):
        #Given the position (pos) of the mouse and whether it's been clicked, determines if button has been pressed
        # Returns is_over, is_clicked
        if self.rect.collidepoint(pos):            
            self.is_over = True
            self.color = self.color2
            
            if state[0]:
                #When the player clicks on the button
                self.pressed = True
                self.released = False
                return True, False
            
            elif not state[0] and self.pressed:
                # If the player has clicked on the button and now lets go
                self.pressed = False
                self.released = True
                return True, True

            elif not state[0] and not self.pressed:
                # If the player isn't currently clicking, nor have they previously
                self.pressed = False
                self.released = False
                return False, False
        
        else:
            self.is_over = False
            self.color = self.color1

            self.released = False
            return False, False
        
    def update(self):
        if self.image != None:
            gbv.screen.blit(self.image, (self.rect[0], self.rect[1]))
        else:
            pygame.draw.rect(gbv.screen, self.color, self.rect)
        #screen.blit(self.image, (self.rect[0], self.rect[1]))


class Pause_Button(Button):
    def __init__(self):
        Button.__init__(self, 1100, 20, 50, 50, (255, 255, 0), (255, 200, 0), img="data/images/ui_elements/pause.png")

        self.states = ["Main", "Pause"]
        self.state = "Main"

    def flip_state(self):
        # Only for pause button
        if self.state == "Pause":
            self.state = "Main"
            self.image = pygame.image.load("data/images/ui_elements/pause.png").convert_alpha()
        elif self.state == "Main":
            self.state = "Pause"
            self.image = pygame.image.load("data/images/ui_elements/play.png").convert_alpha()

    def check_mouse(self, pos, state):
        #Given the position (pos) of the mouse and whether it's been clicked, determines if button has been pressed
        # Returns is_over, is_clicked
        if self.rect.collidepoint(pos):            
            self.is_over = True
            self.color = self.color2
            
            if state[0] and self.released:
                self.pressed = True
                self.released = False
                self.flip_state()
                return True, True
            
            elif not state[0]:
                self.pressed = False
                self.released = True

            return True, False
        
        else:
            self.is_over = False
            self.color = self.color1

            self.released = True
            return False, False