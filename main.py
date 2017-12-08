import pygame

#this first bit is just useful constants
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

fps = 128

screen_size = (1500, 800)

pygame.init()

print('correct test')

disp = pygame.display.set_mode(screen_size)

import player
import room
import overlays
import enemies

size = (12, 8)
seed = enemies.fleye((500, 500))
theme = room.theme()
dif = 1


test_room = room.room(disp, size, seed, theme, dif)

pc = player.player((0,0))
HUD = overlays.hud(pc, disp)
hp = overlays.healthbar(pc, HUD)

test_room.addPlayer(pc)

running = True
while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            pass

    test_room.update()
    test_room.draw_contents(disp)
    test_room.draw_boxes(disp)
    HUD.update(test_room)
    HUD.draw(disp)

    clock = pygame.time.Clock()
    msElapsed = clock.tick(fps)

    pygame.display.update()

    pygame.event.pump()

    #if test_room.enemies():
        #player.hp = 600
        #dif += 1
        #test_room.next_level(dif)
