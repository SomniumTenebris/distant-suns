import pygame
import core_functions as cfunc

def handle_collisions(player, projectileList, masterCollide, asteroidList, 
                        cannon_list, player_list, instaDeathList, enemy_list, explosionList):

    collide = pygame.sprite.spritecollide(player, masterCollide, False, pygame.sprite.collide_circle)
    
    if len(collide) > 0:
        player.thrustTimer = 10
        player.planetCollide(collide[0])#MAKE SURE ONLY ONE PLANET AT A TIME
        
    elif len(collide) <= 0:
        player.hasCollided = False
        player.landed = False
        player.thrustTimer -= 1
     
    collide = pygame.sprite.spritecollide(player, projectileList, False, pygame.sprite.collide_circle)
    for i in collide:
        if i.origin != "Player":
            player.health -= i.damage
            projectileList.remove(i)
            del i

            
    for a in projectileList:
        collide = pygame.sprite.spritecollide(a, masterCollide, False, pygame.sprite.collide_circle)#Change to rendered on screen
        if len(collide) > 0:
            projectileList.remove(a)

            del a

    for a in enemy_list:
        #a.line_of_sight((0, 300), masterCollide, asteroidList)
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
        collide = pygame.sprite.spritecollide(i, projectileList, False, pygame.sprite.collide_circle)
        for a in collide:
            i.health -= a.damage
            projectileList.remove(a)
            del a

