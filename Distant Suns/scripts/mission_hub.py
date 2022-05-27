import pygame

#----- Vision for Mission Hub -----#
# I want this to be a plave where the player checks on current and completed missions
# A scrolling (clean, no bar maybe) area where I can see missions (maybe cool fading text or something)
# Look into better fonts (more sci-fi)
# Highlight current missions, dull out copmleted ones
# Brief descriptions on what each mission calls for/components/factions involved (maybe logos?)
# Looking nice so far. Could add nice cosmetic touches to background (comets, sun, etc) to spruce things up,
# or this could more likely be a tab opening up over the main game window

class Mission():
    def __init__(self, name, description, num_components, component_list, font, screen): #Maybe pass screen in as a parameter?
        self.name = name
        self.font_color = (179, 164, 161)
        self.name_render = font.render(str(name), True, (self.font_color))
        self.rect = self.name_render.get_rect()
        
        self.description = description
        self.description_render = font.render(str(description), True, (self.font_color))
        
        self.components = num_components
        self.section = 1 #Or 0. Basically, how many parts of the quest are completed
        self.component_list = component_list #Conditions for fulfilling the missions

    def draw(self, x, y):
        #Text loping may be an issue
        screen.blit(self.description_render, (x, y))

    def update(self, x, y, isOver, descript_pos):
        self.rect.x, self.rect.y = x, y

        isOver = self.rect.collidepoint(pos)
        if isOver:
            self.font_color = (245, 241, 240)
            self.draw(*descript_pos)
        else:
            self.font_color = (179, 164, 161)

        self.name_render = font.render(str(self.name), True, (self.font_color))
        #+ "  (" + str(self.section) + "/" + str(self.components) + ")"

class MissionHub():
    def __init__(self):
        #----- Main Window Init -----#
        self.image = pygame.image.load("Mission_Hub.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 120, 20

        font = pygame.font.SysFont('ardestineopentype', 52)
        self.title = font.render("Mission Hub", True, (255, 255, 255))
        self.title_offset = [50, 55]

        #----- Scrolling Mission Sidebar -----#

        self.mission_rect = pygame.Rect(55 + self.rect.x, 150 + self.rect.y, 415, 450) #Rect of scrollable area
        self.mission_border = pygame.Rect(self.mission_rect[0] - 5, self.mission_rect[1] - 5,
                                          self.mission_rect[2] + 10, self.mission_rect[3] + 10)
        self.mission_min = -50
        self.mission_max = 0 #max amount of scroll you can do
        self.mission_y = 0
        self.scroll_speed = 10

        self.text_offset = [10, 10]
        self.text_spacing = 40

        #----- Mission Description -----#
        self.descript_pos = [690, 105]

    def new_mission(self, mission):
        pass
    #Call with each new mission. This will add a mission to the mission list, and only then will the hub's max scroll change
        
    def scroll(self, direction):
        #Scrolling up is 1, down is -1
        delta = self.scroll_speed * direction
        if self.mission_y + delta <= self.mission_max and self.mission_y + delta >= self.mission_min:
            self.mission_y += delta


    def update(self, mission_list, mouse_pos):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.title, (self.rect.x + self.title_offset[0],
                                 self.rect.y + self.title_offset[1]))

        pygame.draw.rect(screen, (2, 9, 31), self.mission_border)
        pygame.draw.rect(screen, (8, 24, 69), self.mission_rect)

        for index, mission in enumerate(mission_list):
            x = self.mission_rect.x + self.text_offset[0]
            y = self.mission_rect.y + self.text_offset[1] + self.mission_y + index*self.text_spacing
            
            if y < self.mission_rect.bottom -20 and y > self.mission_rect.top - 10:
                mission.update(x, y, pos, self.descript_pos)
                screen.blit(mission.name_render, (x, y))
         
            

font = pygame.font.SysFont('ardestineopentype', 25)#, bold=True)

hub = MissionHub()
#bg = pygame.image.load("milky_way.jpg").convert()
#bg = pygame.transform.rotozoom(bg, 0, .5)

mission1 = Mission("A long way home", "Find your way home", 3, "player.planet == 'Abyz'", font)
mission2 = Mission("A call from the stars", "Investigate the Cuthulu", 3, "player.planet == 'Abyz'", font)
mission3 = Mission("The wandering soul", "Find your way home", 3, "player.planet == 'Abyz'", font)
mission4 = Mission("For the Yin!", "Investigate the Cuthulu", 3, "player.planet == 'Abyz'", font)
mission5 = Mission("Blood and Sand", "Find your way home", 3, "player.planet == 'Abyz'", font)
mission6 = Mission("Might and Magic", "Investigate the Cuthulu", 3, "player.planet == 'Abyz'", font)
mission7 = Mission("A long way home", "Find your way home", 3, "player.planet == 'Abyz'", font)
mission8 = Mission("A call from the stars", "Investigate the Cuthulu", 3, "player.planet == 'Abyz'", font)
mission9 = Mission("The wandering soul", "Find your way home", 3, "player.planet == 'Abyz'", font)
mission10 = Mission("For the Yin!", "Investigate the Cuthulu", 3, "player.planet == 'Abyz'", font)
mission11 = Mission("Blood and Sand", "Find your way home", 3, "player.planet == 'Abyz'", font)
mission12 = Mission("Might and Magic", "Investigate the Cuthulu", 3, "player.planet == 'Abyz'", font)

mission_list = [mission1, mission2, mission3, mission4, mission5, mission6,
                mission7, mission8, mission9, mission10, mission11, mission12]

while True:
    screen.fill((10, 0, 0))
    #screen.blit(bg, (0, 0))
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEWHEEL:
            hub.scroll(event.y)

    hub.update(mission_list, pos)
    pygame.display.flip()

