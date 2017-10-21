
import pygame
import sys

pygame.init()

#the actual layout of each room is encoded as a list of strings, where each char represents a tile
# these will be looked up in the tileset
testMapCode = ['fffffffffffffff', 'fffffffffffffff', 'fffffffffffffff', 'fffffffffffffff', 'fffffffffffffff', 'fffffffffffffff', 'fffffffffffffff']
outerBounds = ((0, len(testMapCode[0])), (0, len(testMapCode)))
print(outerBounds)

disp = pygame.display.set_mode((1560, 1000))

import room

testRoom = room.room(testMapCode)

import player
pc = player.player((50,50))
npc1 = player.baddy((500,100))
npc2 = player.baddy((900,475))
npc3 = player.baddy((654,346))
npc4 = player.baddy((589,251))
npc5 = player.baddy((123,97))


allSprites = pygame.sprite.Group(pc, npc1)
badguys = pygame.sprite.Group(npc1, npc2, npc3, npc4, npc5)

running = True
while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    disp.blit(testRoom.fSurf, (0,0))
    disp.blit(pc.portrait, pc.move())
    #disp.blit(npc.portrait, npc.move())
    allSprites.draw(disp)
    badguys.draw(disp)


    pygame.display.update()


