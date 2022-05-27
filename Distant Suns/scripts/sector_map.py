import pygame, sys
import math
import core_functions as cfunc
from background import Background

#####################
# Initialize Screen #
#####################
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode([1200, 800])

font = pygame.font.SysFont('ardestineopentype', 25)#, bold=True)

#----- Ideas -----#
# When you click on a planet, it becomes 'selected', and the circle animation plays
# Need an efficient text wrapper
# Need a transition from sector loader to map loader
# Small hover click switch error


class Map():
    # This class is the main screen you see when you open up the map
    # Contains the legend and map data (zoom, pos, etc.)
    def __init__(self, planets):
        #----- Initialization -----#
        self.background = Background()
        self.angle = 0
        self.selected_planet = None #The planet
        self.clicked = False #Whether the user clicked on the selected planet


        #----- Initialize Legend Attributes -----#
        self.legend = pygame.image.load("data/images/misc/map_legend.png")
        self.legend = pygame.transform.rotozoom(self.legend, 0, 0.95) #I think this only converts to inetgers
        self.legend_rect = self.legend.get_rect()
        self.legend_rect[0], self.legend_rect[1] = (-3, -5) #Adjustments to pos
        self.legend_mask = pygame.mask.from_surface(self.legend) #Set colision mask

        #----- Map Attributes -----#
        #-- Set Zoom --#
        self.zoom = 4
        self.zoom_max = 1
        self.zoom_min = 7

        #-- Set Offsets --#
        self.offset = [100, 800] #To allow space for legend
        self.global_coords = [0, 0] #Global coordinates of map

        self.planets = planets #Planets known to player (or sector planets)
        self.font = pygame.font.SysFont('ErasITC', 25)

        #----- Text Offsets for Planet Information -----#
        self.name_pos = (50, 50) # Name of planet
        self.planet_pos = (10, 90) # Image of planet
        self.description_pos = (20, 250)

    def scale(self, magnitude):
        # Zoom the map in and out
        direction = math.copysign(1, magnitude) #Zoom in is 1, out is -1
        test = self.zoom - 0.1*direction
        
        if test <= self.zoom_min and test >= self.zoom_max:
            # If zooming the desired amount would be within zoom bounds
            self.zoom -= direction*1/10
            weight = 40
            self.global_coords[0] -= direction*(weight + 15)
            self.global_coords[1] -= direction*weight

    def drawPlanets(self):
        for i in self.planets:
            i.map_update(self) #Updates the planets on the map
            screen.blit(i.tiny, i.chart_pos)

    def detect_hover(self, pos, knownPlanets, state):
        self.drawPlanets()

        for i in knownPlanets:
            distance = math.hypot(pos[0] - (i.chart_pos[0] + i.tiny_center_x), 
                                pos[1] - (i.chart_pos[1] + i.tiny_center_y))#Add global support, Done
            if distance <= i.map_radius and pos[0] > 250:#If the mouse position is over planet and not over the legend
                self.selected_planet = i
                if state[0]:
                    self.clicked = True                
                break

        else:
            if not self.clicked:
                self.selected_planet = None
            elif state[0]:
                self.selected_planet = None
                self.clicked = False

            
    def update(self):
        pygame.display.set_caption("Map Test")

        #----- Update Angle -----#
        # 'angle' is used for the animated arc rings around planets
        self.angle += 1
        if self.angle > 360:
            self.angle -= 360

        screen.blit(self.legend, (self.legend_rect[0], self.legend_rect[1]))

        if self.selected_planet != None:
            #If the user has selected a planet, draw the animated rings
            cfunc.animated_arc(self.selected_planet, self.angle, (50, 237, 237), self.zoom)

        if self.selected_planet != None:
            self.selected_planet.sidebar_info(self)


###################
# Update Function #
###################

def update_map(knownPlanets, chart, player, button_list, handle_ui):  
    
    screen.fill([0, 10, 15])
    chart.background.update(chart.global_coords)

    ##################
    # Event Handling #
    ##################
    rel = pygame.mouse.get_rel()
    pos = pygame.mouse.get_pos()
    state = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            rel = pygame.mouse.get_rel()
            touching = chart.legend_rect.collidepoint(*pos) and chart.legend_mask.get_at(pos)
            if state[0] and not touching or state[2] and not touching:
                chart.global_coords[0] += chart.zoom*rel[0]
                chart.global_coords[1] += chart.zoom*rel[1]

        elif event.type == pygame.MOUSEWHEEL:
            chart.scale(event.y)

    ###################
    # Draw and Update #
    ###################
    chart.detect_hover(pos, knownPlanets, state)
    chart.update()

    handle_ui(pos, state, button_list, player)
    for button in button_list:
        button.update()



    
