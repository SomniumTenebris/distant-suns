import pygame
import global_vars as gbv

class Fader():
    def __init__(self, direction, speed=1):
        _, _, width, height = gbv.screen.get_rect()
        self.image = pygame.Surface((width, height), flags=pygame.SRCALPHA)
        self.direction = direction*speed

        if self.direction == -1:
            self.alpha = 254
        else:
            self.alpha = 1

        self.active = False

    def update(self):
        self.image.fill((0, 0, 0, self.alpha))
        if self.alpha < 255 and self.alpha > 0:
            self.alpha += self.direction

        gbv.screen.blit(self.image, (0, 0))

        
