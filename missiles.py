import pygame
import spritelings

#START bolts
all_bolt_base = pygame.image.load('projectiles\simple_bolts.png').convert_alpha()
kin_bolt = all_bolt_base.subsurface((1, 1), (70, 70))
melt_bolt = all_bolt_base.subsurface((72, 1), (70, 70))
hot_bolt = all_bolt_base.subsurface((1, 72), (70, 70))
cold_bolt = all_bolt_base.subsurface((143, 1), (70, 70))
bad_bolt = all_bolt_base.subsurface((72, 72), (70, 70))
misc_bolt = all_bolt_base.subsurface((143, 72), (70, 70))
#END bolts

#START blasts
#scales: 32, 48, 64, 80, 96
all_blasts = pygame.image.load('projectiles\simple_blasts.png').convert_alpha()
melty_blast = all_blasts.subsurface((304, 1), (100, 100))
firey_blast = all_blasts.subsurface((1,1), (100, 100))
icey_blast = all_blasts.subsurface((102, 1), (100, 100))
kinetic_shrapnel = all_blasts.subsurface((203, 1), (100, 100))
#END blasts

#BUBBLES

#BURSTS
all_bursts = pygame.image.load('projectiles\simple_bursts.png').convert_alpha()
lava_balls = all_bursts.subsurface((2, 136), (64, 64))
lava_ball = all_bursts.subsurface((15, 216), (32, 32))
acid_balls = all_bursts.subsurface((69, 136), (64, 64))
acid_ball = all_bursts.subsurface((91, 226), (16, 16))
snow_balls = all_bursts.subsurface((136, 136), (64, 64))
snow_ball = all_bursts.subsurface((151, 218), (32, 32))


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
        self.knockback = (0,0)
        self.velocity = (0,0)
        self.acidity = 0
        self.focus_cost = 0
        self.charge_level = caster.charge_level
        self.caster = caster

    def update(self, room):
        self.rect.move_ip(self.caster.velocity)

    def act(self, targets):
        for target in targets:
            target.react(self)
            self.kill()

    def charge(self, power):
        pass

    def fire(self, dir, room):
        print('firing spell')

        self.velocity = (dir[0] * self.velocity_mult,
                        dir[1] * self.velocity_mult)
        self.knockback = (self.velocity[0] * self.knockback_mult,
                          self.velocity[1] * self.knockback_mult)
        print(self.velocity)
        self.caster = self
        room.playerProjectiles.add(self)


#purely cosmetic attachment for giving missiles a cool trail
class trail(missile):
    pass

#dummy class used to represent invisible or oddly shaped hitboxes
class dummy_missile(missile):
    pass


class bolt(missile):
    def __init__(self, caster, img):
        super().__init__(caster, pygame.transform.scale(img, (24, 24)))
        self.knockback_mult = 1/4
        self.velocity_mult = 12
        self.damage = 10
        self.base_img = img

class kinetic_bolt(bolt):
    def __init__(self, caster):
        super().__init__(caster, kin_bolt)
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


    def split(self, room, *args):
        for x in args:
            self.fragment(self).fire( x, room)
        self.kill()

    def react(self, *args):
        self.hp -=1

    def update(self, *args):
        super().update(*args)
        if self.hp<=0:
            self.kill()

    def fire(self, dir, room):
        print(dir)
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
        print('new frag')
        self.velocity_mult = caster.velocity_mult
        self.knockback_mult = caster.knockback_mult
        self.temp = caster.temp
        self.acidity = caster.acidity
        self.damage = caster.damage

class lava_burst(burst):
    def __init__(self, *args):
        super().__init__(*args, lava_balls)
        self.temp = 40
        self.velocity_mult = 7
        self.knockback_mult = 2
        self.fragment = ember

class ember(fragment):
    def __init__(self, *args):
        super().__init__(*args, lava_ball)
        print(self)

class kinetic_burst(burst):
    def __init__(self, *args):
        super().__init__(*args, kinetic_shrapnel)

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
        super().__init__(*args, acid_ball)
        self.timer = 128*5

    def update(self, *args):
        self.timer -=1
        self.velocity = (self.velocity[0] * .8, self.velocity[1] * .8)
        self.rect.move_ip(self.velocity)
        if self.timer <= 0:
            self.kill()
        if self.timer % 8 == 0:
            self.rect.inflate_ip(1,1)



class freezing_burst(burst):
    def __init__(self, *args):
        super().__init__(*args, snow_balls)
        self.temp = -25
        self.velocity_mult = 5
        self.knockback_mult = 1
        self.fragment = COLD_THING

class COLD_THING(fragment):
    def __init__(self, *args):
        super().__init__(*args, snow_ball)





class barrier(missile):
    def __init__(self, caster, img):
        super().__init__(caster, img)



class blast(missile):
    def __init__(self, caster, img):
        super().__init__(caster, pygame.transform.scale(img, (64, 64)))
        self.knockback_mult = 0
        self.velocity_mult = 10
        self.damage = 10
        self.base_img = img


class fire_blast(blast):
    def __init__(self, caster):
        super().__init__(caster, firey_blast)

class ice_blast(blast):
    def __init__(self, caster):
        super().__init__(caster, icey_blast)

class acid_blast(blast):
    def __init__(self, caster):
        super().__init__(caster, melty_blast)

class kinetic_blast(blast):
    def __init__(self, caster):
        super().__init__(caster, kinetic_shrapnel)

