
import pygame
import os
import player
import spritelings
import enemies

tile_scalar = 100

class wall(spritelings.block):
    pass

class fence(wall):
    pass

#finish writing door
class door(spritelings.block):
    def __init__(self, *args):
        pass

    def enter(self):

#finish writing theme and fog_theme
class theme(object):
    def __init__(self):
        floor = pygame.image.load('walls\cobble.png').convert_alpha()
        tlcrnr = pygame.image.load("walls\cnr_stn_tl.png").convert_alpha()
        trcrnr = pygame.image.load("walls\cnr_stn_tr.png").convert_alpha()
        blcrnr = pygame.image.load("walls\cnr_stn_bl.png").convert_alpha()
        brcrnr = pygame.image.load("walls\cnr_stn_br.png").convert_alpha()
        topWall = pygame.image.load("walls\wal_stn_t.png").convert_alpha()
        btmWall = pygame.image.load('walls\wal_stn_b.png').convert_alpha()
        rgtWall = pygame.image.load('walls\wal_stn_r.png').convert_alpha()
        lftWall = pygame.image.load('walls\wal_stn_l.png').convert_alpha()
        # tile set lookup
        self.image_lookup = {'f': floor, 'trc': trcrnr, 'tlc': tlcrnr, 'blc': blcrnr, 'brc': brcrnr, 'tw': topWall, 'bw': btmWall,
                   'rw': rgtWall, 'lw': lftWall}
        self.enemy_lookup = {'basic_baddy':enemies.bouncer}

    def populate(self, seed):
        return self.enemy_lookup['basic_baddy'](70, 70)

class fog_theme(theme):
    def __init__(self):
        super().__init__()
        self.enemy_lookup = {'basic_baddy':enemies.black_bouncer}


size_limit = (16, 11)

#finsih room
class room(object):
    def __init__(self, size, seed, theme,  difficulty, player_spawn= (100, 100), hub = False):
        if hub:
            #hard code the hub world/room
            pass
        else:
            self.sizeX, self.sizeY = size[0], size[1]




        self.allSprites = pygame.sprite.Group()
        self.allProjectiles = pygame.sprite.Group()

        self.player = pygame.sprite.GroupSingle()
        self.playerProjectiles = pygame.sprite.Group()
        self.inactivePlayerProjectiles= pygame.sprite.Group()

        self.enemies = pygame.sprite.Group()
        self.enemyProjectiles = pygame.sprite.Group()

        self.nme_overlays = pygame.sprite.Group()

        self.overlays = pygame.sprite.Group()



    def cleanup(self):
        for x in self.allProjectiles:
            if not self.rect.contains(x.rect):
                #print('deleted a spell')
                x.kill()
                x = None
                #if x:
                    #print('OB spell:', x)


    def addPlayer(self, player):
        self.allSprites.add(player)
        self.player.add(player)

    #supposed to be one of the primary interface methods between sprites/room and level. currently it only adds
    #stuff to allSprites
    def update(self):
        self.allSprites.add(self.enemies, self.player)
        self.allProjectiles.add(self.playerProjectiles, self.enemyProjectiles)
        self.cleanup()
        self.check_collision()

    def check_collision(self):
        player_hitlist_proj = pygame.sprite.groupcollide(self.enemyProjectiles, self.player, 0, 0, spritelings.collide_hitbox)
        if player_hitlist_proj:
            #print(player_hitlist_proj)
            for nme in player_hitlist_proj:
                nme.act(player_hitlist_proj[nme])

        player_hitlist_nme = pygame.sprite.groupcollide(self.enemies, self.player, 0, 0, spritelings.collide_hitbox)
        if player_hitlist_nme:
            #print(player_hitlist_nme)
            for nme in player_hitlist_nme:
                nme.act(player_hitlist_nme[nme])

        enemy_hitlist = pygame.sprite.groupcollide(self.playerProjectiles, self.enemies, 0, 0, spritelings.collide_hitbox)
        if enemy_hitlist:
            #print(enemy_hitlist)
            for bullet in enemy_hitlist:
                bullet.act(enemy_hitlist[bullet])
