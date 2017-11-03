
import pygame
import os
class room():
    '''this stuff is supposed to be present in all instances of rooms in the current level; it will be passed in by the level'''
    '''all of this is the set of all possible things that can be created in this room, and then the associated lookups for keyying them to the mapCode'''
    #set of unique, pre-loaded images with associated keys in the dicTile
    tileSet = []
    floor = pygame.image.load("cobble.png").convert_alpha()
    tlcrnr = pygame.image.load('top_lft_cnr_stnT.png').convert_alpha()
    trcrnr = pygame.image.load('top_rgt_cnr_stnT.png').convert_alpha()
    blcrnr = pygame.image.load('btm_lft_cnr_stnT.png').convert_alpha()
    brcrnr = pygame.image.load('btm_rgt_cnr_stnT.png').convert_alpha()
    topWall = pygame.image.load('top_stn_wallT.png').convert_alpha()
    btmWall = pygame.image.load('btm_stn_wallT.png').convert_alpha()
    rgtWall = pygame.image.load('rgt_stn_wallT.png').convert_alpha()
    lftWall = pygame.image.load('lft_stn_wallT.png').convert_alpha()
    #tile set lookup
    dicTile = {'f': floor, 'trc': trcrnr, 'tlc': tlcrnr, 'blc': blcrnr, 'brc': brcrnr, 'tw': topWall,'bw': btmWall,'rw': rgtWall,'lw': lftWall}

    #set of all possible unique sprites that can appear in this room
    spriteSet = []
    #lookup for the spriteSet
    #spritionary = {'def1': default_enemy_1}

    def __init__(self, mapcode, ):
        self.mapCode = mapcode
        self.xbound = len(self.mapCode[0])*100
        self.ybound = len(self.mapCode)*100
        self.sizeX = len(self.mapCode[0])
        self.sizeY = len(self.mapCode)
        self.outerBounds = ((0, self.xbound), (0, self.ybound))

        #parses the mapcode, assembles the various layers of the visual surface of the room,
        #and saves any special char/script sequences to the internal lists for those things
        self.floorSurf = pygame.Surface((self.xbound, self.ybound))
        self.floorCos = pygame.Surface((self.xbound, self.ybound))
        self.wallSurf = pygame.Surface((self.xbound, self.ybound))
        self.wallCos = pygame.Surface((self.xbound, self.ybound))
        self.obstSurf = pygame.Surface((self.xbound, self.ybound))
        self.topCos = pygame.Surface((self.xbound, self.ybound))
        self.spriteSurf = pygame.Surface((self.xbound, self.ybound))

        for y in range(0, int(self.sizeY)):
            row = mapcode[y]
            for x in range(0, int(self.sizeX)):
                space = row[x]
                if space == '<':

                    self.floorSurf.blit(self.dicTile[space], (x * 100, y * 100))
                else:
                    self.floorSurf.blit(self.dicTile[space], (x * 100, y * 100))

        for i in range(0, self.xbound, 100):
            self.wallSurf.blit(self.dicTile['tw'], (i, 0))

        for j in range(0, self.ybound, 100):
            self.wallSurf.blit(self.dicTile['rw'], (i, j))

        for i in range(0, self.xbound, 100):
            self.wallSurf.blit(self.dicTile['bw'], (i, j))

        for j in range(0, self.ybound, 100):
            self.wallSurf.blit(self.dicTile['lw'], (0, j))

        self.wallSurf.blit(self.dicTile['tlc'], (0, 0))
        self.wallSurf.blit(self.dicTile['blc'], (0, self.ybound - 100))
        self.wallSurf.blit(self.dicTile['brc'], (self.xbound - 100, self.ybound - 100))
        self.wallSurf.blit(self.dicTile['trc'], (self.xbound - 100, 0))
        self.wallSurf.set_colorkey((0,0,0))

        self.fSurf = pygame.Surface((self.xbound, self.ybound))
        self.fSurf.blit(self.floorSurf, (0,0))
        self.fSurf.blit(self.wallSurf, (0,0))
