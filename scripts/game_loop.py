import pygame, sys
import core_functions as cfunc
import global_vars as gbv
import effects as effects

g_locx = g_locy = 0
thrust = True

def main_loop(clock, background, player, camera,
              projectileList, loadedPlanets, masterCollide, instaDeathList,
              enemy_list, cannon_list, explosionList, asteroidList, player_list):

    global thrust, g_locx, g_locy
    
    clock.tick(60)
    gbv.screen.fill([10, 0, 30])
    background.update(camera.g_loc)

################
# Player Input #
################

    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        state = pygame.mouse.get_pressed()
        
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:#and thrust == True:
                player.held_up = True
                
                if thrust == True:
                    player.thrust()
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.held_left = True

            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
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

            elif event.key == pygame.K_x: #I'm trying to compile an error report
                print(player.velocity)

        if event.type == pygame.MOUSEMOTION:#Delete if not using
            pos = pygame.mouse.get_pos()

        if state[0] == True:
            player.shoot(projectileList)

        if state[2] == True:
            player.warpDrive()

##########################
# Update Player Movement #
##########################

    if player.held_up == True: #Eventually add deceleration
        player.thrust()
    if player.held_left == True:
        player.turn(1)
    if player.held_right == True:
        player.turn(-1)

###########
# Gravity #
###########

    if player.landed == False: #Limit radius of influence somehow
        for i in loadedPlanets:
           player.gravity(i)


########################
# Planetary Collisions #
########################

    collide = pygame.sprite.spritecollide(player, masterCollide, False, pygame.sprite.collide_circle)
    
    if len(collide) > 0:
        collided = True
        player.thrustTimer = 10
        player.planetCollide(collide[0])#MAKE SURE ONLY ONE PLANET AT A TIME
        player.hasCollided = True
        if player.landed == False:#If you hit a planet while not landed, you cannot thrust
            thrust = False
    elif len(collide) <= 0:
        player.hasCollided = False
        player.landed = False
        collided = False
        player.thrustTimer -= 1
        if player.thrustTimer == 0:
            thrust = True

####################
# Updating Sprites #
####################

    for i in explosionList: #Maybe render under planets
        i.update(explosionList)

    for i in masterCollide:
        i.update(camera.g_loc)

    for i in enemy_list:
        #i.stateHandler(Saudor)
        i.update(camera.g_loc)

    for i in projectileList:#Optimize later
        i.update()


    #star.update(camera.g_loc)
        
    g_locx, g_locy = camera.update(player, g_locx, g_locy) #Update camera and global coordinates

##############
# Collisions #
##############


    #If a bullet collides with the player 
    collide = pygame.sprite.spritecollide(player, projectileList, False, pygame.sprite.collide_circle)
    for i in collide:
        if i.origin != "Player":#fix l8r
            player.health -= i.damage
            projectileList.remove(i)
            del i

            
    for a in projectileList:
        collide = pygame.sprite.spritecollide(a, masterCollide, False, pygame.sprite.collide_circle)#Change to rendered on screen
        if len(collide) > 0:
            projectileList.remove(a)

            del a

    for a in enemy_list:
        collide = pygame.sprite.spritecollide(a, projectileList, False, pygame.sprite.collide_circle)
        for i in collide:
            if i.origin != "Enemy":#fix l8r, 
                a.health -= i.damage
                projectileList.remove(i)
                del i

    for i in asteroidList:
        i.update()
        collide = pygame.sprite.spritecollide(i, asteroidList, False, pygame.sprite.collide_circle)
        collide.remove(i)

        for a in collide:
            j, k = cfunc.bounce(i, a)
            cfunc.vel_update(i, j)
            cfunc.vel_update(a, k)

        collide = pygame.sprite.spritecollide(i, player_list, False, pygame.sprite.collide_circle)

        for a in collide:
            j, k = cfunc.bounce(i, a)
            cfunc.vel_update(i, j)
            cfunc.vel_update(player, k)
            player.damage(i)

        collide = pygame.sprite.spritecollide(i, projectileList, False, pygame.sprite.collide_circle)
        for a in collide:
            j, k = cfunc.bounce(i, a)
            cfunc.vel_update(i, j)
            i.health -= a.damage
            projectileList.remove(a)
            del a


        collide = pygame.sprite.spritecollide(i, masterCollide, False, pygame.sprite.collide_circle)
        for a in collide:
            asteroidList.remove(i)
            del i
            
    collide = pygame.sprite.spritecollide(player, instaDeathList, False, pygame.sprite.collide_circle)
    if len(collide) > 0:
        player.health = 0
            
    for i in cannon_list:
        i.update(camera.g_loc, projectileList)

        if cfunc.trig3(player, i)[3] < 1000:
            i.cannon.moveTo(player)
            
        collide = pygame.sprite.spritecollide(i, projectileList, False, pygame.sprite.collide_circle)
        for a in collide:
            i.health -= a.damage
            projectileList.remove(a)
            del a


    for i in player_list:
        i.update(camera.g_loc, masterCollide)


#######################################
# Cleanup, Deletion, and Optimization #
#######################################

    if player.health <= 0 and player.alive == True:
        player.alive = False
        explosion = effects.Explosion(player.pos, 2) 
        explosionList.append(explosion)#When explosion animation stops, the player dies. Big sad
        player_list.remove(player)
        
    for i in enemy_list:
        if i.health <= 0:
            enemy_list.remove(i)
            explosionList.append(effects.Explosion((i.pos), 2))
            del i

    for i in asteroidList:
        if i.health <= 0:
            i.split()
            del i

    for i in cannon_list:
        if i.health <= 0:
            cannon_list.remove(i)
            explosionList.append(effects.Explosion((i.pos), 2))
            del i

    pygame.display.update(projectileList.draw(gbv.screen))
    player.HUD.update(player)

    pygame.display.flip()

