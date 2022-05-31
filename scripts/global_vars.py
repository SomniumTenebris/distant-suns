import pygame
pygame.init()

# Possibly scale ui elements to HEIGHT and WIDTH to allow for screen size changes
width = 1200
height = 800

screen = pygame.display.set_mode([width, height])

font = pygame.font.SysFont('ardestineopentype', 25)
