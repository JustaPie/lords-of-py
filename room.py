
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
                             3:enemies.blind_bouncer, 4:enemies.fleye, 5:enemies.lugg,
                             6:enemies.sneyeper, 7:enemies.blue_sneyeper}

    def populate(self, space, budget, predef = None):
        from random import randint
        difficulty = 0
        pop = pygame.sprite.Group()
        if predef:
            return predef
        while difficulty<budget:
            species = randint(0, 7)
            level = randint(1, 5)
            x = randint(space.left, space.right)
            y = randint(space.top, space.bottom)
            newb = self.enemy_lookup[species]((x,y), level)
            pop.add(newb)
            difficulty+= newb.assess()
        return pop


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
    def __init__(self, screen, size, predef, theme,  difficulty, player_spawn= (100, 100), hub = False):
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

        self.enemies = pygame.sprite.Group(self.theme.populate(self.rect, difficulty*10, predef))
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
            for xy in y.hitboxes:
                pygame.draw.rect(disp, green, xy, 2)

        for z in test_room.allProjectiles:
            pygame.draw.rect(disp, red, z.rect, 7)
            pygame.draw.rect(disp, green, z.hitbox, 4)

    def next_level(self, player,  difficulty):
        self.enemies.add(self.theme.populate(self.rect, (difficulty*10)))
        for each in self.enemies:
            each.set_target(player)
