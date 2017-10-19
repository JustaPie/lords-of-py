
import pygame
import sys

pygame.init()

#the actual layout of each room is encoded as a list of strings, where each char represents a tile
# these will be looked up in the tileset
testMapCode = ['fffff', 'fffff', 'fffff', 'fffff']
outerBounds = ((0, len(testMapCode[0])), (0, len(testMapCode)))
print(outerBounds)

disp = pygame.display.set_mode((1280, 768))

import room

testRoom = room.room(testMapCode)

running = True
while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    disp.blit(testRoom.fSurf, (0,0))

    pygame.display.update()
