'''
this is a bunch of test stuff to see how algorithms would work
'''

from pygame.locals import *

'''
so, major question:
would we rather have a larger tileset (and thus have to load more images every time it changed)
or a smaller tileset, and just rotate the reusable tiles (such as corners and walls)?
rotating means that every time we use them, it''l cost us whatever time it takes to rotate something
loading is (i assume) more expensive, but only needs to be done once every time we alter the tileSet.
we could just load one image, then rotate it and save each rotation?'''


#mapcode parser. We should think about making rooms a child class of display or surface, to avoid having to pass them in as params when we need to draw them on the screen
def buildRoom(mapCode):
    import pygame, sys



    pygame.init()

    finalSurf = pygame.display.set_mode((1280,768))

    white = (0, 0, 0)

    floor = pygame.image.load('cobble.png').convert_alpha()
    tlcrnr = pygame.image.load('top_lft_cnr_stnT.png').convert_alpha()
    trcrnr = pygame.image.load('top_rgt_cnr_stnT.png').convert_alpha()
    blcrnr = pygame.image.load('btm_lft_cnr_stnT.png').convert_alpha()
    brcrnr = pygame.image.load('btm_rgt_cnr_stnT.png').convert_alpha()
    topWall = pygame.image.load('top_stn_wallT.png').convert_alpha()
    btmWall = pygame.image.load('btm_stn_wallT.png').convert_alpha()
    rgtWall = pygame.image.load('rgt_stn_wallT.png').convert_alpha()
    lftWall = pygame.image.load('lft_stn_wallT.png').convert_alpha()


    #this is the tileSet, which will be a dictionary of keys that will be used across all levels, and mapped to other images as needed.
    #we should figure out how many/what sort of keys we need.
    tileSet = {'f': floor, 'trc': trcrnr, 'tlc': tlcrnr, 'blc': blcrnr, 'brc': brcrnr, 'tw': topWall,'bw': btmWall,'rw': rgtWall,'lw': lftWall}

    coX = len(mapCode[0])
    coY = len(mapCode)

    #so, currently everything is in scalings of 10 or 100, but I think we would be better off shifting to multiples of 8 and 64
    #I think pygame might be scaling to that level already, which is why the current output looks disjointed.
    sizeX = coX*100
    sizeY = coY*100
    #have to set up bounds for reasons, also a display surface.
    floorSurf = pygame.Surface((sizeX , sizeY ))
    wallSurf = pygame.Surface((sizeX , sizeY ))

    #so bounds aren't useful until we have stuff to keep inside them
    bounds = ((50, sizeX-50) , (50, sizeY-50))


    #my plan was to have each room contain several surfaces/layers that would be drawn ontp of each in layers
    #this makes occlusion easier, as we only have to get our alphas/transparencies right and itll handle itself
    # plus, I figure it might be faster to render, because the room will be broken into layers, so if we
    #only need to change a thing on one layer, we can alter that and keep the others constant.
    for y in range(0,coY):
        row = list(mapCode[y])
        for x in range(0, coX):
            space = row[x]
            floorSurf.blit(tileSet[space], (x *100,y *100))

    wallSurf.blit(floorSurf, (0,0))
    for i in range(0, sizeX , 100):
        wallSurf.blit(tileSet['tw'], (i, 0))

    for j in range(0, sizeY , 100):
        wallSurf.blit(tileSet['rw'], (i, j))

    for i in range(0, sizeX , 100):
        wallSurf.blit(tileSet['bw'], (i, j))

    for j in range(0, sizeY , 100):
        wallSurf.blit(tileSet['lw'], (0, j))

    wallSurf.blit(tileSet['tlc'], (0, 0))
    wallSurf.blit(tileSet['blc'], (0, sizeY-100))
    wallSurf.blit(tileSet['brc'], (sizeX -100, sizeY -100))
    wallSurf.blit(tileSet['trc'], (sizeX -100, 0))


    running = True
    while (running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        finalSurf.blit(floorSurf, (0,0))
        finalSurf.blit(wallSurf, (0,0))
        pygame.display.update()


#this is the mapCode I was talking about. in this incarnation, walls are implicitly placed around the rectangle defined by the room
# but that need not necessarily be the case. we can handle them any numbers of ways, It mostly comes down to how we want to
# format our mapCode.
room = ['fffff', 'fffff', 'fffff']


buildRoom(room)