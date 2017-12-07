<<<<<<< HEAD

import pygame
import os
import player
import spritelings

tile_scalar = 100

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
        self.xbound = len(self.mapCode[0])*tile_scalar
        self.ybound = len(self.mapCode)*tile_scalar
        self.sizeX = len(self.mapCode[0])
        self.sizeY = len(self.mapCode)
        self.outerBounds = (self.xbound, self.ybound)
        #self.rect = pygame.Rect.get_rect(self.outerBounds)

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

                    self.floorSurf.blit(self.dicTile[space], (x * tile_scalar, y * tile_scalar))
                else:
                    self.floorSurf.blit(self.dicTile[space], (x * tile_scalar, y * tile_scalar))

        for i in range(0, self.xbound, tile_scalar):
            self.wallSurf.blit(self.dicTile['tw'], (i, 0))

        for j in range(0, self.ybound, tile_scalar):
            self.wallSurf.blit(self.dicTile['rw'], (i, j))

        for i in range(0, self.xbound, tile_scalar):
            self.wallSurf.blit(self.dicTile['bw'], (i, j))

        for j in range(0, self.ybound, tile_scalar):
            self.wallSurf.blit(self.dicTile['lw'], (0, j))

        self.wallSurf.blit(self.dicTile['tlc'], (0, 0))
        self.wallSurf.blit(self.dicTile['blc'], (0, self.ybound - tile_scalar))
        self.wallSurf.blit(self.dicTile['brc'], (self.xbound - tile_scalar, self.ybound - tile_scalar))
        self.wallSurf.blit(self.dicTile['trc'], (self.xbound - tile_scalar, 0))
        self.wallSurf.set_colorkey((0,0,0))

        self.fSurf = pygame.Surface((self.xbound, self.ybound))
        self.fSurf.blit(self.floorSurf, (0,0))
        self.fSurf.blit(self.wallSurf, (0,0))

        self.rect = self.fSurf.get_rect()

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
=======

import pygame

import enemies
import missiles
import spritelings

tile_scalar = 100
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

class wall(spritelings.block):
    def __init__(self, facing,  *args):
        super(wall, self).__init__(*args)
        #hitbox_lookup = {'up': , 'down': , 'left': ,'right': }
        self.facing = facing
        self.damage = 0
        if facing == 'up':
            self.hitbox = self.rect.inflate(0, -(self.rect.height*.65))
            self.hitbox.top = self.rect.top
        elif facing == 'down':
            self.hitbox = self.rect.inflate(0, -(self.rect.height * .65))
            self.hitbox.bottom = self.rect.bottom
        elif facing == 'left':
            self.hitbox = self.rect.inflate(-(self.rect.width*0.65), 0)
            self.hitbox.left = self.rect.left
        elif facing == 'right':
            self.hitbox = self.rect.inflate(-(self.rect.width*0.65), 0)
            self.hitbox.right = self.rect.right
        self.hitboxes = [self.hitbox]

    def act(self, targets):
        facing = self.facing
        for target in targets:
            if isinstance(target, missiles.missile):
                self.overlays.add(target.impact(target.rect.center))
                if not target.contact:
                    target.hit()
                    target.contact = True
                else:
                    target.kill()
            else:
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
                target.react(self)



class corner(spritelings.block):
    def __init__(self, facing, *args):
        super().__init__(*args)
        self.hitbox = self.rect.inflate(-(self.rect.width * 0.5), -(self.rect.height*0.5))
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

class floor(spritelings.block):
    def __init__(self, *args):
        super().__init__(*args)

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
        self.enemy_lookup = {0:enemies.bouncer, 1:enemies.black_bouncer, 2:enemies.blue_bouncer,
                             3:enemies.blind_bouncer, 4:enemies.fleye, 5:enemies.lugg}

    def populate(self, space):
        from random import randint
        return self.enemy_lookup[randint(0, 5)](space)

    def build(self, border):
        all_walls = pygame.sprite.Group()
        for i in range(border.left, border.right, tile_scalar):
            all_walls.add(wall('up', self.image_lookup['tw'], (i+50, border.top)))
            all_walls.add(wall('down', self.image_lookup['bw'], (i+50, border.bottom)))
        for j in range(border.top, border.bottom, tile_scalar):
            all_walls.add(wall('left', self.image_lookup['lw'], (border.left, j+50)))
            all_walls.add(wall('right', self.image_lookup['rw'], (border.right, j+50)))

        all_walls.add(corner('top_left', self.image_lookup['tlc'], border.topleft))
        all_walls.add(corner('bottom_left', self.image_lookup['blc'], border.bottomleft))
        all_walls.add(corner('top_right', self.image_lookup['trc'], border.topright))
        all_walls.add(corner('bottom_right', self.image_lookup['brc'], border.bottomright))


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
class room(pygame.sprite.Sprite):
    def __init__(self, screen, size, seed, theme,  difficulty, player_spawn= (100, 100), hub = False):
        super(room, self).__init__()
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

        self.image = self.floorSurf
        self.rect = self.image.get_rect()
        self.rect.center = screen.get_rect().center
        self.floor = pygame.sprite.Group(floor(self.image, self.rect.center))

        self.allSprites = pygame.sprite.Group()
        self.allProjectiles = pygame.sprite.Group()

        self.walls = theme.build(self.rect)

        self.player = pygame.sprite.GroupSingle()
        self.playerProjectiles = pygame.sprite.Group()
        self.inactivePlayerProjectiles= pygame.sprite.Group()

        self.enemies = pygame.sprite.Group(self.theme.populate(self.rect.center))
        self.enemyProjectiles = pygame.sprite.Group()

        self.nme_overlays = pygame.sprite.Group()

        self.overlays = pygame.sprite.Group()
        self.allActors= pygame.sprite.Group()





    def cleanup(self):
        for x in self.allProjectiles:
            if not self.rect.contains(x.rect):
                x.hit()
                x.kill()
                x = None
                #if x:
                    #print('OB spell:', x)


    def addPlayer(self, player):
        self.allSprites.add(player)
        self.player.add(player)
        for baddy in self.enemies:
            baddy.set_target(player)
        if not self.rect.contains(player.rect):
            player.rect.top = self.rect.top
            player.rect.left = self.rect.left

    #supposed to be one of the primary interface methods between sprites/room and level. currently it only adds
    #stuff to allSprites
    def update(self):
        self.allSprites.add(self.player,
                            self.enemies,
                            self.nme_overlays,
                            self.overlays
                            )
        self.allActors.add(self.player, self.enemies)
        self.allProjectiles.add(self.playerProjectiles,
                                self.inactivePlayerProjectiles,
                                self.enemyProjectiles
                                )
        self.allSprites.update(self)
        self.allProjectiles.update(self)

        #self.cleanup()
        self.check_collision()

    def draw_contents(self, disp):
        self.floor.draw(disp)
        self.walls.draw(disp)
        self.enemies.draw(disp)
        self.nme_overlays.draw(disp)
        self.player.draw(disp)
        self.inactivePlayerProjectiles.draw(disp)
        self.overlays.draw(disp)
        self.enemyProjectiles.draw(disp)
        self.playerProjectiles.draw(disp)


    def check_collision(self):
        wall_bumps = pygame.sprite.groupcollide(self.walls, self.allActors, 0, 0, spritelings.collide_hitbox)
        if wall_bumps:
            print(wall_bumps)
            for manatee in wall_bumps:
                manatee.act(wall_bumps[manatee])

        wall_shots = pygame.sprite.groupcollide(self.walls, self.allProjectiles, 0, 0, spritelings.collide_hitbox)
        if wall_shots:
            for misses in wall_shots:
                misses.act(wall_shots[misses])

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

    def draw_boxes(self, disp):
        test_room = self
        for w in test_room.walls:
            pygame.draw.rect(disp, green, w.rect, 4)
            pygame.draw.rect(disp, red, w.hitbox, 4)

        for x in test_room.player:
            pygame.draw.rect(disp, green, x.rect, 4)
            pygame.draw.rect(disp, red, x.hitbox, 4)

        for y in test_room.enemies:
            pygame.draw.rect(disp, blue, y.rect, 8)
            pygame.draw.rect(disp, red, y.hitbox, 4)

        for z in test_room.allProjectiles:
            pygame.draw.rect(disp, red, z.rect, 7)
            pygame.draw.rect(disp, green, z.hitbox, 4)
>>>>>>> Logan's-Stuff
