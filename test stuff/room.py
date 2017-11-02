
import pygame
import os
import player

class room():
    '''this stuff is supposed to be present in all instances of rooms in the current level; it will be passed in by the level'''
    '''all of this is the set of all possible things that can be created in this room, and then the associated lookups for keyying them to the mapCode'''
    #set of unique, pre-loaded images with associated keys in the dicTile

    floor = pygame.image.load('walls\cobble.png').convert_alpha()
    tlcrnr = pygame.image.load("walls\cnr_stn_tl.png").convert_alpha()
    trcrnr = pygame.image.load("walls\cnr_stn_tr.png").convert_alpha()
    blcrnr = pygame.image.load("walls\cnr_stn_bl.png").convert_alpha()
    brcrnr = pygame.image.load("walls\cnr_stn_br.png").convert_alpha()
    topWall = pygame.image.load("walls\wal_stn_t.png").convert_alpha()
    btmWall = pygame.image.load('walls\wal_stn_b.png').convert_alpha()
    rgtWall = pygame.image.load('walls\wal_stn_r.png').convert_alpha()
    lftWall = pygame.image.load('walls\wal_stn_l.png').convert_alpha()
    #tile set lookup
    dicTile = {'f': floor, 'trc': trcrnr, 'tlc': tlcrnr, 'blc': blcrnr, 'brc': brcrnr, 'tw': topWall,'bw': btmWall,'rw': rgtWall,'lw': lftWall}

    def __init__(self, mapcode):
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

        self.rect = self.fSurf.get_rect()

        self.allSprites = pygame.sprite.Group()
        self.allProjectiles = pygame.sprite.Group()

        self.player = pygame.sprite.Group()
        self.playerProjectiles = pygame.sprite.Group()

        self.enemies = pygame.sprite.Group()
        self.enemyProjectiles = pygame.sprite.Group()



    def cleanup(self):
        for x in self.allProjectiles:
            if not self.rect.contains(x.rect):
                print('deleted a spell')
                x.kill()
                x = None
                if x:
                    print('OB spell:', x)


    def addPlayer(self, player):
        self.allSprites.add(player)
        self.player.add(player)

    def update(self):
        self.allSprites.add(self.enemies, self.player)
        self.allProjectiles.add(self.playerProjectiles, self.enemyProjectiles)
        self.cleanup()

