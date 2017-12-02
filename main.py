import pygame

#this first bit is just useful constants
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

plyr_loc = (100, 100)
nme1_loc = (500, 500)
fps = 128
screen_size = (1600, 1100)

pygame.init()

print('correct test')

disp = pygame.display.set_mode(screen_size)

import player
import room
import missiles
import enemies
import overlays

test_room_code = ['ffffffffffffffff','fffffffffffffffff','fffffffffffffffff',
                  'fffffffffffffffff','fffffffffffffffff','fffffffffffffffff',
                  'fffffffffffffffff','fffffffffffffffff','fffffffffffffffff',
                  'fffffffffffffffff', 'fffffffffffffffff']


test_room = room.room(test_room_code)

pc = player.player(plyr_loc)
HUD = overlays.hud(pc, disp)
hp = overlays.healthbar(pc, HUD)

test_room.addPlayer(pc)

bumper = enemies.black_bouncer((600, 600))
bumper.set_target(pc)
test_room.enemies.add(bumper)

#test_room.overlays.add(hp)

'''
fleye1 = enemies.fleye((500, 500))
test_room.enemies.add(fleye1)
fleye1.set_target(pc)

''''''
fleye2 = enemies.fleye((400, 400))
test_room.enemies.add(fleye2)
fleye2.set_target(pc)

fleye3 = enemies.fleye((600, 600))
test_room.enemies.add(fleye3)
fleye3.set_target(pc)
'''

running = True
while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            pass

    disp.blit(test_room.fSurf, (0,0))

    test_room.player.update(test_room)
    test_room.playerProjectiles.update(test_room)

    test_room.enemies.update(test_room)
    test_room.enemyProjectiles.update(test_room)

    test_room.allSprites.draw(disp)
    test_room.allProjectiles.draw(disp)

    test_room.inactivePlayerProjectiles.update(test_room)
    test_room.inactivePlayerProjectiles.draw(disp)

    test_room.nme_overlays.draw(disp)

    HUD.update(test_room)
    HUD.draw(disp)

    #player_hud.update()
    #player_hud.show(disp)

    for x in test_room.player:
        pygame.draw.rect(disp, green, x.rect, 4)
    for x in test_room.player:
        pygame.draw.rect(disp, red, x.hitbox, 4)

    for y in test_room.enemies:
        pygame.draw.rect(disp, blue, y.rect, 8)
    for y in test_room.enemies:
        pygame.draw.rect(disp, red, y.hitbox, 4)
        for z in y.hitboxes:
            pygame.draw.rect(disp, green, z, 5)

    for z in test_room.allProjectiles:
        pygame.draw.rect(disp, red, z.rect, 7)
    for z in test_room.allProjectiles:
        pygame.draw.rect(disp, green, z.hitbox, 4)


    test_room.update()


    clock = pygame.time.Clock()
    msElapsed = clock.tick(fps)

    pygame.display.update()

    pygame.event.pump()
