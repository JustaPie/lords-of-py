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
all_blasts = pygame.image.load('projectiles\simple_blasts.png').convert_alpha()
acid_blast = all_blasts.subsurface((304, 1), (100, 100))
firey_blast = all_blasts.subsurface((1,1), (100, 100))
ice_blast = all_blasts.subsurface((102, 1), (100, 100))
kinetic_shrapnel = all_blasts.subsurface((203, 1), (100, 100))
#END blasts

#BUBBLES

#BURSTS

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
        self.power = 1
        self.max_power = 100
        self.charge_rate = .1
        self.caster = caster

    def update(self, room):
        self.rect.move_ip(self.caster.velocity)

    def act(self, target):
        target.react(self)
        self.kill()

    def act(self, target_list):
        for target in target_list:
            target.react(self)
            self.kill()

    def fire(self, dir, room):
        print('firing spell')

        self.velocity = (dir[0] * self.velocity_mult,
                        dir[1] * self.velocity_mult)
        self.knockback = (self.velocity[0] * self.knockback_mult,
                          self.velocity[1] * self.knockback_mult)
        print(self.velocity)
        self.caster = self


class bolt(missile):
    def __init__(self, caster, img):
        super().__init__(caster, pygame.transform.scale(img, (14, 14)))
        self.knockback_mult = 1/4
        self.velocity_mult = 18



class kinetic_bolt(bolt):
    def __init__(self, caster):
        super().__init__(caster, kin_bolt)
        self.knockback_mult = 1/2
        self.velocity_mult = 24


class fire_bolt(bolt):
    def __init__(self, caster):
        super().__init__(caster, hot_bolt)
        self.temp = 30


class ice_bolt(bolt):
    def __init__(self, caster):
        super().__init__(caster, cold_bolt)
        self.temp = -30


class acid_bolt(bolt):
    def __init__(self, caster):
        super().__init__(caster, melt_bolt)
        self.acidity = 20