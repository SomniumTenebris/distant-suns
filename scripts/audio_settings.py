import pygame, sys
import global_vars as gbv
from button import Button
from slider import Slider

class AudioPopup():
    def __init__(self):
        self.image = pygame.image.load("data/images/ui_elements/ui_popup.png").convert_alpha()
        self.rect = self.image.get_rect()

        #----- Center Image -----#
        screen_center = (gbv.width/2, gbv.height/2)
        width, height = self.rect[2], self.rect[3]
        self.pos = (screen_center[0]-(width/2), screen_center[1]-(height/2))

        #----- Render Title/Text -----#
        self.font = pygame.font.SysFont('ErasITC', 25)
        self.slider_font = pygame.font.SysFont('ErasITC', 20)
        self.title = self.font.render("Audio Settings", True, (0, 0, 0))
        self.title_pos = (self.pos[0] + 20, self.pos[1] + 30)

        #----- Create Widgits -----#
        self.music_slider = Slider("Music", self.pos[0]+60, self.pos[1]+100, 250, 50, 0, 100, (10, 40, 20), (255, 0, 0), self.slider_font)
        self.sfx_slider = Slider("SFX", self.pos[0]+60, self.pos[1]+150, 250, 50, 0, 100, (10, 40, 20), (255, 0, 0), self.slider_font)
        self.sliders = [self.music_slider, self.sfx_slider]

        self.exit_button = Button(self.pos[0]+330, self.pos[1]+40, 30, 30, (255, 0, 0), (255, 30, 30), "Main", img="data/images/ui_elements/exit.png")
        self.buttons = [self.exit_button]

    def update(self):
        gbv.screen.blit(self.image, self.pos)
        gbv.screen.blit(self.title, self.title_pos)

        self.music_slider.update()
        self.sfx_slider.update()