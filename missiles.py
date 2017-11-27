import pygame
import spritelings

missile_sheet = pygame.image.load('projectiles\simple_missiles.png').convert_alpha()

hot_bolt = missile_sheet.subsurface((1,1), (66, 66))
melt_bolt = missile_sheet.subsurface((68, 1), (66, 66))
cold_bolt = missile_sheet.subsurface((135, 1),(66, 66))

lava_balls = missile_sheet.subsurface((1, 135),(66,66))
lava_ball = missile_sheet.subsurface((1, 202),(66,66))

snow_balls = missile_sheet.subsurface((135, 135),(66, 66))
snow_ball = missile_sheet.subsurface((135, 202),(66, 66))

acid_balls = missile_sheet.subsurface((68, 135),(66, 66))
acid_ball = missile_sheet.subsurface((68, 202),(66, 66))

tri_bolt = missile_sheet.subsurface((202, 1),(66, 66))
quad_bolt = missile_sheet.subsurface((202, 68),(66,66))
penta_bolt = missile_sheet.subsurface((202, 135),(66,66))
hex_bolt = missile_sheet.subsurface((202, 202),(66,66))

idle_flame = missile_sheet.subsurface((2,69), (64, 36))
idle_cloud = missile_sheet.subsurface((79,73),(43,46))
snow_flakes = missile_sheet.subsurface((164, 103), (29, 15))


#BEAMS/RAYS
all_rays = pygame.image.load('projectiles\simple_rays.png').convert_alpha()
hot_rays = all_rays.subsurface((0,0),(56, 18))
cold_rays = all_rays.subsurface((0,19),(56, 18))
acid_rays = all_rays.subsurface((0,38),(56, 18))
hot_ray_1 = hot_rays.subsurface((0,0), (18, 18))
cold_ray_1 = cold_rays.subsurface((0,0), (18, 18))

class missile(spritelings.entity):
    def __init__(self, caster, img):
        super().__init__(img, caster.rect.center)

        self.damage = 0
        self.temp = 0
        self.knockback_mult = 0
        self.knockback = (0,0)
        self.velocity = (0,0)
        self.acidity = 0
        self.focus_cost = 0
        #self.charge_level = caster.charge_level
        self.caster = caster
        self.hitbox = self.rect

    def update(self, room):
        if not self.velocity:
            self.kill()
        self.rect.move_ip(self.caster.velocity)
        self.hitbox.center = self.rect.center

    def act(self, targets):
        self.knockback = (self.velocity[0] * self.knockback_mult,
                          self.velocity[1] * self.knockback_mult)
        for target in targets:
            target.react(self)
        #self.kill()

    def charge(self, power):
        pass

    def fire(self, dir, team):
        self.velocity = (dir[0] * self.velocity_mult,
                        dir[1] * self.velocity_mult)
        self.caster = self
        team.add(self)


#purely cosmetic attachment for giving missiles a cool trail
class trail(missile):
    def __init__(self, *args):
        super().__init__(*args)


#dummy class used to represent invisible or oddly shaped hitboxes
class dummy_missile(missile):
    pass



class cloud(missile):
    def __init__(self, size,  *args):
        super().__init__(*args, pygame.transform.scale(idle_cloud, (size, size)))
        self.acidity = 15
        self.duration = 36 * size/8
        self.velocity = (0,0)

    def update(self, *args):
        self.duration-= 1
        if self.duration <= 0:
            self.kill()

class flame(missile):
    def __init__(self, *args):
        super().__init__(*args, idle_flame)
        self.temp = 15

    def react(self, *args):
        super().react(args)

class snowflake(missile):
    def __init__(self, *args):
        super().__init__(*args, snow_flakes)
        self.temp = -15


########################
#####   BOLTS   ########
########################
class bolt(missile):
    def __init__(self, caster, img):
        super().__init__(caster, pygame.transform.scale(img, (24, 24)))
        self.knockback_mult = 1/4
        self.velocity_mult = 12
        self.damage = 10
        self.base_img = img

class kinetic_bolt(bolt):
    def __init__(self, caster):
        super().__init__(caster, tri_bolt)
        self.knockback_mult = 1/2
        self.velocity_mult = 16


class fire_bolt(bolt):
    def __init__(self, caster):
        super().__init__(caster, hot_bolt)
        self.temp = 25


class ice_bolt(bolt):
    def __init__(self, caster):
        super().__init__(caster, cold_bolt)
        self.temp = -25


class acid_bolt(bolt):
    def __init__(self, caster):
        super().__init__(caster, melt_bolt)
        self.acidity = 20


###########################
###       BURSTS        ###
###########################

class burst(missile):
    def __init__(self, caster, img):
        super().__init__(caster, img)
        self.hp = 6


    def split(self, team, *args):
        for x in args:
            self.fragment(self).fire( x, team)
        self.kill()

    def react(self, *args):
        self.hp -=1

    def update(self, *args):
        super().update(*args)
        if self.hp<=0:
            self.kill()

    def fire(self, dir, room):
        sprd = 2
        if not dir[1]:
            self.split(room, (dir[0]*sprd, dir[1]), (dir[0]*sprd, -1), (dir[0]*sprd, 1))
        elif dir[0] and dir[1]:
            self.split(room, (dir[0]*sprd, dir[1]*sprd), (dir[0], dir[1]*sprd), (dir[0]*sprd, dir[1]))
        else:
            self.split(room, (dir[0], dir[1]*sprd), (-1, dir[1]*sprd), (1, dir[1]*sprd))

class fragment(missile):
    def __init__(self, caster, img):
        super().__init__(caster, img)
        self.velocity_mult = caster.velocity_mult
        self.knockback_mult = caster.knockback_mult
        self.temp = caster.temp
        self.acidity = caster.acidity
        self.damage = caster.damage
        '''center = self.rect.center
        self.rect = self.rect.inflate(-32, -32)
        self.hitbox = self.rect.inflate(-40, -40)
        self.rect.center = center
        self.hitbox.center = center'''

class lava_burst(burst):
    def __init__(self, *args):
        super().__init__(*args, lava_balls)
        self.temp = 40
        self.velocity_mult = 7
        self.knockback_mult = 2
        self.fragment = ember

class ember(fragment):
    def __init__(self, *args):
        super().__init__(*args, lava_ball.subsurface((13,14), (33,33)))

        #print(self)

class atomic_burst(burst):
    def __init__(self, *args):
        super().__init__(*args, acid_balls)
        self.acidity = 30
        self.velocity_mult = 40
        self.knockback_mult = 0
        self.fragment = acid_bubble

    def fire(self, dir, room):
        sprd = 2
        if not dir[1]:
            self.split(room, dir, (dir[0]*sprd, dir[1]), (dir[0], -1), (dir[0], 1), (dir[0]*sprd, -1), (dir[0]*sprd, 1))
        elif dir[0] and dir[1]:
            self.split(room, dir, (dir[0]*sprd, dir[1]*sprd), (0, dir[1]), (dir[0], 0), (0, dir[1]*sprd), (dir[0]*sprd, 0))
        else:
            self.split(room, dir, (dir[0]*sprd, dir[1]), (-1, dir[1]), (1, dir[1]), (-1, dir[1]*sprd), (1, dir[1]*sprd))

class acid_bubble(fragment):
    def __init__(self, *args):
        super().__init__(*args, pygame.transform.scale(acid_ball, (20, 20)))
        self.timer = 128*5
        self.size = 24

    def update(self, room):
        self.timer -=1
        self.velocity = (self.velocity[0] * .8, self.velocity[1] * .8)
        self.rect.move_ip(self.velocity)
        if self.timer <= 0:
            room.playerProjectiles.add(cloud(int(self.size*1.2), self))
            self.kill()
        if self.timer % 8 == 0:
            center = self.rect.center
            self.size += 1
            self.rect.inflate_ip(1,1)
            self.image = pygame.transform.scale(acid_ball, (self.size, self.size))
            self.rect.center = center
    def react(self, bastard):
        super().react(bastard)
        self.timer = 0
    def act(self, *args):
        super().act(*args)
        self.timer = 0



class freezing_burst(burst):
    def __init__(self, *args):
        super().__init__(*args, snow_balls)
        self.temp = -25
        self.velocity_mult = 5
        self.knockback_mult = 1
        self.fragment = COLD_THING

class COLD_THING(fragment):
    def __init__(self, *args):
        super().__init__(*args, snow_ball.subsurface((13,14), (33,33)))





class barrier(missile):
    def __init__(self, caster, img):
        super().__init__(caster, img)


