import pygame
import global_vars as gbv
import core_functions as cfunc

# NOTE: Starting to think that I'll need to make a seperate UI elements folder/file

class Slider():
    def __init__(self, title, x, y, length, current_value, min_value, max_value, bar_color, slider_color, font):
        self.length = length
        self.height = 10
        self.rect = [x, y, length, self.height]

        border = 10
        self.collide_rect = pygame.Rect(x-border, y-border, length+2*border, self.height+2*border)

        self.radius = 10
        # Radius of clickable slider object

        self.current_value = current_value
        self.min_value = min_value
        self.max_value = max_value

        self.slider_pos = (self.current_value/(self.min_value+self.max_value))*self.length + self.rect[0]

        self.slider_color = slider_color
        self.bar_color = bar_color

        self.title_render = font.render(title, True, (0, 0, 0))
        self.title_pos = (x, y-30)

    def is_over(self, pos, state):
        # Tests to see if mouse is over the slider circle
        if state[0]:
            _, distance = cfunc.trig(pos, (self.slider_pos, self.rect[1]+self.radius/2))
            if distance < self.radius or self.collide_rect.collidepoint(pos):
                adjusted_x_pos = pos[0] - self.rect[0]
                if adjusted_x_pos > 0 and adjusted_x_pos < self.length:
                    self.slider_pos = pos[0]
           

    def move_slider(self):
        self.slider_pos = (self.current_value/(self.min_value+self.max_value))*self.length + self.rect[0]


    def update(self):
        gbv.screen.blit(self.title_render, self.title_pos)
        pygame.draw.rect(gbv.screen, self.bar_color, self.rect)
        pygame.draw.circle(gbv.screen, self.slider_color, (self.slider_pos, self.rect[1]+self.radius/2), self.radius)

