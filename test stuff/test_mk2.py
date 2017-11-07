import pygame

red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

pygame.init()

disp = pygame.display.set_mode((1560, 1000))

import player
import room
import badguy
import missiles

test_room_code = ['ffffffffffffffff','fffffffffffffffff','fffffffffffffffff','fffffffffffffffff','fffffffffffffffff','fffffffffffffffff','fffffffffffffffff','fffffffffffffffff','fffffffffffffffff','fffffffffffffffff']


test_room = room.room(test_room_code)

pc = player.player((100, 100))

test_room.addPlayer(pc)

maskPos = (300, 300)
mask1 = badguy.mask_of_death(maskPos)
#mask2 = badguy.mask_of_death(maskPos)
test_room.enemies.add(mask1)

running = True
while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    disp.blit(test_room.fSurf, (0,0))

    test_room.player.update(test_room)
    test_room.playerProjectiles.update()

    test_room.enemies.update(test_room)
    test_room.enemyProjectiles.update()

    test_room.allSprites.draw(disp)
    test_room.allProjectiles.draw(disp)

    for x in test_room.player:
        pygame.draw.rect(disp, red, x.rect, 4)

    for y in test_room.enemies:
        pygame.draw.rect(disp, blue, y.rect, 4)

    for z in test_room.allProjectiles:
        pygame.draw.rect(disp, green, z.rect, 4)


    test_room.update()


    clock = pygame.time.Clock()
    msElapsed = clock.tick(128)

    pygame.display.update()
