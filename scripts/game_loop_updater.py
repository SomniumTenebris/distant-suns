import pygame
import core_functions as cfunc
import effects


def update(player, player_list, loadedPlanets, explosionList,
           masterCollide, enemy_list, projectileList,
           camera, cannon_list, asteroidList, screen, background, button_list, fader, chart):

    screen.fill([10, 0, 30])
    background.update(camera.g_loc)

    chart.global_coords = player.pos
    chart.zoom = 1
    # This sets the initial camera position to view the player
    
    if player.landed == False: #Limit radius of influence somehow
        for i in loadedPlanets:
           player.gravity(i)

    for i in explosionList: #Maybe render under planets
        i.update(explosionList)

    for i in masterCollide:
        i.update(camera.g_loc)

    for i in enemy_list:
        i.update(camera.g_loc)
        i.stateHandler(masterCollide, player, enemy_list)

    for i in projectileList:#Optimize later
        i.update(camera.g_loc)

    camera.update(player) #Update camera and global coordinates

    for i in player_list:
        i.update(camera.g_loc, masterCollide)

    for i in cannon_list:
        i.update(camera.g_loc, projectileList)
        # Crappy way of inducing range, fix l8r
        if cfunc.trig3(player, i)[3] < 1000:
            i.cannon.moveTo(player)

    if player.health <= 0 and player.alive == True: #Only trigger first time
        player.alive = False
        explosion = effects.Explosion(player.pos, 2) 
        explosionList.append(explosion)#When explosion animation stops, the player dies. Big sad
        player_list.remove(player)
        fader.active = True
        
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

    pygame.display.update(projectileList.draw(screen))
    player.HUD.update(player)

    for button in button_list:
        button.update()

    if fader.active:
        fader.update()