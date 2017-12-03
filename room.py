
import pygame
import os
import player
import spritelings
import enemies

tile_scalar = 100

class wall(spritelings.block):
    def __init__(self, facing,  *args):
        super(wall, self).__init__(*args)
        #hitbox_lookup = {'up': , 'down': , 'left': ,'right': }
        self.facing = facing
        if facing == 'up':
            self.hitbox = self.rect.inflate(0, -(self.rect.height*.5))
            self.hitbox.top = self.rect.top
        elif facing == 'down':
            self.hitbox = self.rect.inflate(0, -(self.rect.height * .5))
            self.hitbox.bottom = self.rect.bottom
        elif facing == 'left':
            self.hitbox = self.rect.inflate(-(self.rect.width*05.), 0)
            self.hitbox.left = self.rect.left
        elif facing == 'right':
            self.hitbox = self.rect.inflate(-(self.rect.width*05.), 0)
            self.hitbox.right = self.rect.right

    def act(self, target):
        facing = self.facing
        if facing == 'up':
            target.hitbox.top = self.hitbox.bottom
            #target.hitbox.bottom = self.hitbox.top
            #target.hitbox.left = self.hitbox.right
            #target.hitbox.right = self.hitbox.left
            target.rect.center = target.hitbox.center
        elif facing == 'down':
            #target.hitbox.top = self.hitbox.bottom
            target.hitbox.bottom = self.hitbox.top
            #target.hitbox.left = self.hitbox.right
            #target.hitbox.right = self.hitbox.left
            target.rect.center = target.hitbox.center
        elif facing == 'left':
            #target.hitbox.top = self.hitbox.bottom
            #target.hitbox.bottom = self.hitbox.top
            target.hitbox.left = self.hitbox.right
            #target.hitbox.right = self.hitbox.left
            target.rect.center = target.hitbox.center
        elif facing == 'right':
            #target.hitbox.top = self.hitbox.bottom
            #target.hitbox.bottom = self.hitbox.top
            #target.hitbox.left = self.hitbox.right
            target.hitbox.right = self.hitbox.left
            target.rect.center = target.hitbox.center

class corner(spritelings.block):
    def __init__(self, facing, *args):
        super().__init__(*args)
        self.hitbox = self.rect.inflate(-(self.rect.width * 05.), -(self.rect.height*0.5))
        if facing == 'top_left':
            self.hitbox.top = self.rect.top
            #self.hitbox.bottom = self.rect.bottom
            self.hitbox.left = self.rect.left
            #self.hitbox.right = self.rect.right
        elif facing == 'top_right':
            self.hitbox.top = self.rect.top
            #self.hitbox.bottom = self.rect.bottom
            #self.hitbox.left = self.rect.left
            self.hitbox.right = self.rect.right
        elif facing == 'bottom_right':
            #self.hitbox.top = self.rect.top
            self.hitbox.bottom = self.rect.bottom
            #self.hitbox.left = self.rect.left
            self.hitbox.right = self.rect.right
        elif facing == 'bottom_left':
            #self.hitbox.top = self.rect.top
            self.hitbox.bottom = self.rect.bottom
            self.hitbox.left = self.rect.left
            #self.hitbox.right = self.rect.right


class fence(wall):
    pass

#finish writing door
class door(spritelings.block):
    def __init__(self, *args):
        pass

    def enter(self):
        pass

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

    def build(self, size):
        all_walls = pygame.sprite.Group()
        for i in range(0, size[0]*100, tile_scalar):
            all_walls.add(wall('up', self.image_lookup['tw'], (i, 0)))

        for j in range(0, size[1]*100, tile_scalar):
            all_walls.add(wall('right', self.image_lookup['rw'], (i, j)))

        for i in range(0, size[0]*100, tile_scalar):
            all_walls.add(wall('bottom', self.image_lookup['bw'], (i, j)))

        for j in range(0, size[1]*100, tile_scalar):
            all_walls.add(wall('left', self.image_lookup['lw'], (i, 0)))

        return all_walls

class fog_theme(theme):
    def __init__(self):
        super().__init__()
        self.enemy_lookup = {'basic_baddy':enemies.black_bouncer}

class hub_theme(theme):
    def __init__(self):
        super(hub_theme, self).__init__()

size_limit = (16, 11)


#finsih room
class room(object):
    def __init__(self, size, seed, theme,  difficulty, player_spawn= (100, 100), hub = False):
        if hub:
            pass
        else:
            self.sizeX, self.sizeY = size[0], size[1]
            self.floorSurf = pygame.Surface((self.sizeX*100, self.sizeY*100))
            self.floorCos = pygame.Surface((self.sizeX*100, self.sizeY*100))
            self.wallSurf = pygame.Surface((self.sizeX*100, self.sizeY*100))
            self.wallCos = pygame.Surface((self.sizeX*100, self.sizeY*100))
            self.obstSurf = pygame.Surface((self.sizeX*100, self.sizeY*100))
            self.topCos = pygame.Surface((self.sizeX*100, self.sizeY*100))
            self.spriteSurf = pygame.Surface((self.sizeX*100, self.sizeY*100))
            self.theme = theme

            for y in range(0, int(self.sizeY)):
                for x in range(0, int(self.sizeX)):
                        self.floorSurf.blit(self.theme.image_lookup['f'], (x * tile_scalar, y * tile_scalar))

        self.fSurf = self.floorSurf
        self.rect = self.fSurf.get_rect()

        self.allSprites = pygame.sprite.Group()
        self.allProjectiles = pygame.sprite.Group()

        self.walls = theme.build(size)

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

    def draw(self, disp):
        pass

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
