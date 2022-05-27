import pygame
import global_vars as gbv
from time import sleep

############
# Text Box #
############

class dialogueBox():#Once it's called, it's initiated.
    def __init__(self, text, image):#SET X AND Y BEFOREHAND
        font = pygame.font.SysFont('ErasITC', 25)


        BG_COLOR = pygame.Color('gray12')
        BLUE = pygame.Color('dodgerblue')
        box = pygame.image.load("TextBox.png").convert_alpha()
        boxRect = box.get_rect()

        textOffset = 0
        hasRendered = []
        TxtWidth = 30 #Distance from edge of text box
        TxtHeight = 70

        box_x = 200
        box_y = 500

        # Triple quoted strings contain newline characters.
        self.text_orig = text

        # Create an iterator so that we can get one character after the other.

        textList = self.text_orig.split("&")

        for i in range(0, len(textList)):
            text_iterator = iter(textList[i])
            text = ''

            done = False
            while not done:
                sleep(.01)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    # Press 'r' to reset the text. Eliminate in actual version
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            text_iterator = iter(self.text_orig)
                            text = ''

                if len(text) < len(textList[i]):
                    text += next(text_iterator)

                else:
                    hasRendered.append(text)
                    done = True



                gbv.screen.blit(box, (box_x, box_y))

                Character = pygame.image.load(image)
                gbv.screen.blit(Character, (375 + box_x, 50 + box_y))

                for b in range(0, len(hasRendered)):
                    img = font.render(hasRendered[b], True, BLUE)  # Recognizes newline characters.
                    gbv.screen.blit(img, (box_x + TxtWidth, box_y + 70 + 30*b))

                img = font.render(text, True, BLUE)
                gbv.screen.blit(img, (box_x + 30, box_y + 70 + 30*i))

                #pygame.display.update(projectileList.draw(gbv.screen))
                #pygame.display.update(masterCollide.draw(gbv.screen))
                #pygame.display.update(asteroidList.draw(gbv.screen))
                
                #player.stop()
                #player.update()

                
                pygame.display.flip()
                    
    def wait():#Animate box while waiting
        run = True
        while run:
            
            for event in pygame.event.get():
                key = pygame.key.get_pressed()
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    run = False
            pygame.display.flip()
