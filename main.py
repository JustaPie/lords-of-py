import pygame

#this first bit is just useful constants
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

plyr_loc = (100, 100)
nme1_loc = (500, 500)
fps = 128
screen_size = (1500, 800)

pygame.init()

print('correct test')

disp = pygame.display.set_mode(screen_size)

import player
import room
import enemies
import overlays

size = (12, 8)
seed = 124
theme = room.theme()
dif = 1


test_room = room.room(disp, size, seed, theme, dif)

pc = player.player(plyr_loc)
HUD = overlays.hud(pc, disp)
hp = overlays.healthbar(pc, HUD)

test_room.addPlayer(pc)

bumper = enemies.lugg((600, 600))
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

    test_room.update()
    test_room.draw_contents(disp)
    test_room.draw_boxes(disp)
    HUD.update(test_room)
    HUD.draw(disp)



    #test_room.update()
    #test_room.draw(disp)


    clock = pygame.time.Clock()
    msElapsed = clock.tick(fps)

    pygame.display.update()

    pygame.event.pump()
