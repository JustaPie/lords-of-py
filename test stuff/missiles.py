import spritelings
import pygame

pygame.init()

acid_orb_l = pygame.image.load('projectiles\disin_orb_l.png').convert_alpha()
acid_orb_m = pygame.image.load('projectiles\disin_orb_m.png').convert_alpha()
acid_orb_s = pygame.image.load('projectiles\disin_orb_s.png').convert_alpha()

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

    def update(self):
        self.rect.move_ip(self.velocity)



#exploding projectile
class blast(missile):
    pass


#instantaneous straight line laser attack
class beam(missile):
    pass


#short-range, conical shotgun spread
class burst(missile):
    pass



class barrier(missile):
    pass