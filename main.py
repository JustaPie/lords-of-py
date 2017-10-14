
import pygame, sys

from pygame.locals import *

def trial1():
    pygame.init()

    dispSurf = pygame.display.set_mode((1000, 1000))

    pygame.display.set_caption('trial 1')

    xpos = 10
    ypos = 10
    xsiz = 20
    ysiz = 20

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        pygame.draw.rect(dispSurf, (0, 255, 0), (xpos, ypos, xsiz, ysiz))
        if(xpos<990):
            xpos + 1


def trial2():
    pygame.init()

    white = (255, 255, 255)

    dispX = 1200
    dispY = 768
    screen = pygame.display.set_mode((dispX,dispY))
    pygame.display.set_caption('trial 2')

    player = pygame.image.load('pc_cR.png').convert_alpha()
    floor = pygame.image.load('cobble.png').convert()
    player1 = pygame.image.load('pc_cR1.png').convert_alpha()
    player2 = pygame.image.load('pc_cR2.png').convert_alpha()
    player3 = pygame.image.load('pc_cR3.png').convert_alpha()
    walkCycle = [player1, player2, player1, player3]

    psizy = player.get_height()
    psizx = player.get_width()

    r = 0
    g = 0
    b = 0

    screen.fill((r, g, b))

    xpos = 10
    ypos = 10
    ysiz = floor.get_height()
    xsiz = floor.get_width()
    cycle = 0

    roomH = 10
    roomW = 10


    running = True
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            ypos -= 1
            cycle += 1
        if key[pygame.K_s]:
            ypos += 1
            cycle += 1
        if key[pygame.K_a]:
            xpos -= 1
            cycle += 1
        if key[pygame.K_d]:
            xpos += 1
            cycle += 1

        screen.fill((r, g, b))
        for x in range(0, dispX, xsiz):
            for y in range(0, dispY, ysiz):
                screen.blit(floor, (x,y))

        if(xpos<0):
            xpos=0
        if(xpos >(dispX - psizx)):
            xpos=(dispX - psizx)
        if (ypos < 0):
            ypos = 0
        if (ypos > (dispY - psizy)):
            ypos = (dispY - psizy)

        screen.blit(walkCycle[cycle % 4], (xpos, ypos))

        #pygame.time.Clock.tick(60)
        pygame.display.update()



    pygame.quit()


trial2()