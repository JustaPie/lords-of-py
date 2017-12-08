from random import *

import pygame

import overlays
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

def reduce(this, by):
    x = this[0]-(this[0]*by)
    y = this[1]-(this[1]*by)
    return (x, y)

class missile(spritelings.entity):
    def __init__(self, caster, img):
        super().__init__(img, caster.rect.center)
        self.cast_from = self.rect.center
        self.damage = 0
#I'm currently considering phasing out knockback in favor of either stopping_power (a basic slowing effect) or
# a much simpler form. I want shots to feel like they have impact: when something gets hit, it has to visibly react
#to the impact, but knockback is sorta clumsy, and produces erratic behavior, such as enemies rocketing off-screen
#when hit
        self.knockback_mult = 0
        self.knockback = (0,0)
        self.slow_rate = 0
        self.velocity = (10,10)
        self.velocity_mult = 1
        self.focus_cost = 0
        #self.charge_level = caster.charge_level
        self.caster = caster
        self.hitbox = self.rect.inflate(-(self.rect.width*0.5), -(self.rect.height * 0.5))
        self.hitbox.center = self.rect.center
        self.impact = overlays.generic_impact
        self.contact = False

    class burn(object):
        def __init__(self, ignite_chance):
            print('doin a burn')
            self.match = 'burn'
            self.ignite_chance = ignite_chance
            self.duration = 128 * randint(0, 10)
            #subject.cond_queue.add(self)

        def __call__(self, subject):
            print('callin a burn')
            self.duration -= 1
            ignite_on = randint(0, 1000)
            ignite = self.ignite_chance >= ignite_on
            if ignite:
                subject.apply(subject.burning(self.duration))
                return False
            elif self.duration <= 1:
                return False
            else:
                self.duration = self.duration/2
                return True

        def extend(self, burn):
            self.duration += burn.duration
            self.ignite_chance = max(self.ignite_chance, burn.ignite_chance)

    class melt(object):
        def __init__(self, acidity):
            self.acidity = acidity

        def __call__(self, subject):
            subject.armor -= subject.armor * 1/(self.acidity * 100)
            return False

        def extend(self, blah):
            pass

    class freeze(object):
        def __init__(self, magnitude):
            print('doin a freeze')
            self.match = 'freeze'
            self.magnitude = magnitude
            self.duration = 128 * 3

        def __call__(self, subject):
            print('callin a freeze')
            freeze_factor = (self.magnitude - abs(subject.max_cold) )/ abs(subject.max_cold)
            print(freeze_factor)
            if freeze_factor >=1:
                self.duration = 128 * 10
                subject.apply(subject.frozen(self.duration))
                print('freezing something')
            else:
                print('slowing something')
                x, y = subject.velocity[0], subject.velocity[1]
                x, y = int(x*freeze_factor), int(y*freeze_factor)
                subject.velocity = (x, y)

            self.duration -= 1
            if self.duration <= 0:
                self.magnitude = 0
                return False
            return True

        def extend(self, freezie):
            print('extendin a freeze')
            self.magnitude += freezie.magnitude
            if self.duration < 128 * 3:
                self.duration = 128 * 3

    class flash(object):
        pass

    class stagger(object):
        pass

    class knockback2(object):
        pass


    def update(self, room):
        room.overlays.add(self.overlays)
        self.rect.move_ip(self.caster.velocity)
        self.hitbox.center = self.rect.center
        self.cast_from = self.rect.center


    def act(self, targets):
        self.knockback = (self.velocity[0] * self.knockback_mult,
                          self.velocity[1] * self.knockback_mult)
        for target in targets:
            target.react(self)
            for effect in self.effects:
                effect(target)
        self.overlays.add(self.impact(self.rect.center))
        if abs(self.velocity[0]) <= 1 and abs(self.velocity[1]) <= 1 :
            print(self, "has stopped")
            self.kill()

    def charge(self, power):
        pass

    def fire(self, dir, team):
        self.velocity = (dir[0] * self.velocity_mult,
                        dir[1] * self.velocity_mult)
        self.caster = self
        team.add(self)

    def hit(self):
        if not self.contact:
            self.overlays.add(self.impact(self.rect.center, 32))
            self.contact = True

########################
#####   BOLTS   ########
########################
class bolt(missile):
    def __init__(self, caster, img):
        super().__init__(caster, pygame.transform.scale(img, (24, 24)))
        self.knockback_mult = 1/4
        self.velocity_mult = 12
        self.damage = 4
        self.base_img = img

class kinetic_bolt(bolt):
    def __init__(self, caster):
        super().__init__(caster, hex_bolt)
        self.knockback_mult = 1/2
        self.velocity_mult = 16

    def update(self, room):
        super().update(room)


    def act(self, targets):
        super(kinetic_bolt, self).act(targets)



class fire_bolt(bolt):
    def __init__(self, caster):
        super().__init__(caster, hot_bolt)
        self.damage = 2
        self.effects.append(self.burn(15))
        self.impact = overlays.fiery_impact


class ice_bolt(bolt):
    def __init__(self, caster):
        super().__init__(caster, cold_bolt)
        self.damage = 2
        self.effects.append(self.freeze(15))
        self.impact = overlays.cold_impact


class acid_bolt(bolt):
    def __init__(self, caster):
        super().__init__(caster, melt_bolt)
        self.effects.append(self.melt(10))
        self.impact = overlays.acid_impact


###########################
###       BURSTS        ###
###########################

class burst(missile):
    def __init__(self, caster, img):
        super().__init__(caster, img)
        self.hp = 60


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
        self.cast_from = self.rect.center
        sprd = 3
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
        self.effects = caster.effects
        self.damage = caster.damage
        self.impact = caster.impact


class lava_burst(burst):
    def __init__(self, *args):
        super().__init__(*args, lava_balls)
        self.velocity_mult = 7
        self.knockback_mult = .6
        self.fragment = ember
        self.effects.append(self.burn(7))
        self.impact = overlays.fiery_impact
        self.damage = 2

class ember(fragment):
    def __init__(self, *args):
        super().__init__(*args, lava_ball.subsurface((13,14), (33,33)))



class atomic_burst(burst):
    def __init__(self, *args):
        super().__init__(*args, acid_balls)
        self.velocity_mult = 40
        self.knockback_mult = 0
        #self.effects.append(self.melt(10))
        self.fragment = acid_bubble
        self.impact = overlays.generic_impact
        self.team = None

    def fire(self, dir, room):
        self.cast_from = self.rect.center
        sprd = randint(0, 4)
        self.team = room
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
        self.damage = 5
        #self.effects.append(self.melt(6))
        print("my caster is: ", self.caster, "my center is: ", self.rect.center)

    def update(self, room):
        if not self.team:
            self.team = room.playerProjectiles
        self.timer -=1
        self.velocity = (self.velocity[0] * .8, self.velocity[1] * .8)
        self.rect.move_ip(self.velocity)
        center = self.rect.center
        if self.timer <= 0:
            print("exploding at: ", self.rect.center)
            self.team.add(cloud(int(self.size*1.2), self))
            self.kill()
        if self.timer % 8 == 0:

            self.size += 1
            self.rect.inflate_ip(1,1)
            self.hitbox.inflate_ip(1,1)
            self.image = pygame.transform.scale(acid_ball, (self.size, self.size))
            self.rect.center = center
            self.hitbox.center = center

    def react(self, bastard):
        super().react(bastard)
        self.timer = 0
    def act(self, *args):
        super().act(*args)
        self.timer = 0



class freezing_burst(burst):
    def __init__(self, *args):
        super().__init__(*args, snow_balls)
        self.velocity_mult = 5
        self.knockback_mult = .2
        self.fragment = COLD_THING
        self.effects.append(self.freeze(12))
        self.impact = overlays.cold_impact
        self.damage = 3

class COLD_THING(fragment):
    def __init__(self, *args):
        super().__init__(*args, snow_ball.subsurface((13,14), (33,33)))


'''
#tri_bolt = missile_sheet.subsurface((202, 1),(66, 66))
#quad_bolt = missile_sheet.subsurface((202, 68),(66,66))
#penta_bolt = missile_sheet.subsurface((202, 135),(66,66))
#hex_bolt = missile_sheet.subsurface((202, 202),(66,66))
'''
sides = {6:hex_bolt, 5:penta_bolt, 4:quad_bolt, 3:tri_bolt}

class kinetic_splitter(missile):
    def __init__(self, *args, points = 6):
        super().__init__(*args, pygame.transform.scale(sides[points], (32, 32)))
        self.points = points
        self.velocity_mult = 10

    def act(self, targets):
        super().act(targets)






class barrier(missile):
    def __init__(self, caster, img):
        super().__init__(caster, img)


########################################################################################################################
######   MISC AND COSMETIC          ####################################################################################
########################################################################################################################

#purely cosmetic attachment for giving missiles a cool trail
###might re-class the trail to serve as the parent of snowflakes, etc.
class trail(missile):
    def __init__(self, *args):
        super().__init__(*args)

class cloud(missile):
    def __init__(self, size,  *args):
        super().__init__(*args, pygame.transform.scale(idle_cloud, (size, size)))
        self.effects.append(self.melt(6))
        self.damage = 2
        self.duration = 36 * size/8
        print("my caster is: ", self.caster, "my center is: ", self.rect.center)
        self.velocity = (0,0)

    def update(self, *args):

        self.hitbox.center = self.rect.center
        self.duration-= 1
        if self.duration <= 0:
            self.kill()

class flame(missile):
    def __init__(self, *args):
        super().__init__(*args, idle_flame)
        self.image_lookup = {0: missile_sheet.subsurface((54,69), (11,35)),
                             1:missile_sheet.subsurface((43, 76), (9,27)),
                             2:missile_sheet.subsurface((29,71), (11,33)),
                             3:missile_sheet.subsurface((16,77), (11,26)),
                             4:missile_sheet.subsurface((4,71), (9,32))}

class snowflake(missile):
    def __init__(self, *args):
        super().__init__(*args, snow_flakes)
        self.temp = -15


#dummy class used to represent invisible or oddly shaped hitboxes
class dummy_missile(missile):
    pass


