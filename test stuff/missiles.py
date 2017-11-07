import spritelings
import pygame

pygame.init()

acid_orb_l = pygame.image.load('projectiles\disin_orb_l.png').convert_alpha()
acid_orb_m = pygame.image.load('projectiles\disin_orb_m.png').convert_alpha()
acid_orb_s = pygame.image.load('projectiles\disin_orb_s.png').convert_alpha()

fire_ball_l = pygame.image.load('projectiles\dfire_ball_l.png').convert_alpha()
fire_ball_m = pygame.transform.scale(fire_ball_l, (64, 64))
fire_ball_s = pygame.transform.scale(fire_ball_l, (32, 32))

ice_disc_l = pygame.image.load('projectiles\ice_disc_l.png').convert_alpha()
ice_disc_m = pygame.transform.scale(ice_disc_l, (64, 64))
ice_disc_s = pygame.transform.scale(ice_disc_l, (32, 32))


kin_bolt = pygame.image.load('projectiles\kin_bolt.png').convert_alpha()
kin_bolt = pygame.transform.scale(kin_bolt, (32, 32))

'''
class actor(entity):
def __init__(self, pos, img, size):
   super().__init__(pos, img.subsurface((0,0), size))
   self.velocity = (0, 0)
'''


class missile(spritelings.actor):
    def __init__(self, caster, img):
        super().__init__(img, caster.pos)



#most basic missile/projectile. A small circle/square that travels out and hits things.
class bolt(missile):
    def __init__(self, caster, img):
        super().__init__(caster, img)
        self.damage = 10

    def update(self):
        self.rect.move_ip(self.velocity)

    def act(self, target):
        target.react(self)
        self.kill()

    def act(self, target_list):
        for target in target_list:
            target.react(self)
            self.kill()


class kinetic_bolt(bolt):
    def __init__(self, caster, vel):
        super().__init__(caster, kin_bolt)

        xVel = vel[0] *14
        yVel = vel[1] *14
        self.velocity = (xVel, yVel)
        caster.cooldown += 15
        xk = self.velocity[0]/7
        yk = self.velocity[1]/7
        self.knockback = (xk, yk)


class fire_bolt(bolt):
    def __init__(self, caster, vel):
        super().__init__(caster, fire_ball_m)

        xVel = vel[0] * 10
        yVel = vel[1] * 10
        self.velocity = (xVel, yVel)
        caster.cooldown += 30
        xk = self.velocity[0] / 10
        yk = self.velocity[1] / 10
        self.knockback = (xk, yk)


class ice_bolt(bolt):
    def __init__(self, caster, vel):
        super().__init__(caster, ice_disc_m)

        xVel = vel[0] * 10
        yVel = vel[1] * 10
        self.velocity = (xVel, yVel)
        caster.cooldown += 30
        xk = self.velocity[0] / 10
        yk = self.velocity[1] / 10
        self.knockback = (xk, yk)


class acid_bolt(bolt):
    def __init__(self, caster, vel):
        super().__init__(caster, acid_orb_m)

        xVel = vel[0] * 10
        yVel = vel[1] * 10
        self.velocity = (xVel, yVel)
        caster.cooldown += 30
        xk = self.velocity[0] / 10
        yk = self.velocity[1] / 10
        self.knockback = (xk, yk)


#exploding projectile
class blast(missile):
    pass


#instantaneous straight line laser attack
class beam(missile):
    def __init__(self, caster, img):
        super().__init__(caster, img)

    def update(self):
        self.rect.move_ip(self.velocity)

class kinetic_beam(beam):
    def __init__(self, caster, vel):
        super().__init__(caster, kin_bolt)

        xVel = vel[0] * 14
        yVel = vel[1] * 14
        self.velocity = (xVel, yVel)
        caster.cooldown += 15
        xk = self.velocity[0] / 7
        yk = self.velocity[1] / 7
        self.knockback = (xk, yk)


#short-range, conical shotgun spread
class burst(missile):
    pass



class barrier(missile):
    pass