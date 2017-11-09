import spritelings
import pygame

pygame.init()

#all of this is pre-loading projectile images, and when we go into final production, this will
#likely have to be parred down heavily
acid_orb_l = pygame.image.load('projectiles\disin_orb_l.png').convert_alpha()
acid_orb_m = pygame.transform.scale(acid_orb_l, (64, 64))
acid_orb_s = pygame.transform.scale(acid_orb_l, (32, 32))

fire_ball_l = pygame.image.load('projectiles\dfire_ball_l.png').convert_alpha()
fire_ball_m = pygame.transform.scale(fire_ball_l, (64, 64))
fire_ball_s = pygame.transform.scale(fire_ball_l, (32, 32))

ice_disc_l = pygame.image.load('projectiles\ice_disc_l.png').convert_alpha()
ice_disc_m = pygame.transform.scale(ice_disc_l, (64, 64))
ice_disc_s = pygame.transform.scale(ice_disc_l, (32, 32))


kin_bolt = pygame.image.load('projectiles\kin_bolt.png').convert_alpha()
kin_bolt = pygame.transform.scale(kin_bolt, (32, 32))

#START bolts
#END bolts

#START beams

beam_delay = 10
kin_beam = pygame.image.load('projectiles\kin_beam_full.png').convert_alpha()
kin_beam_origin = kin_beam.subsurface((45, 235), (42, 20))
kin_beam_body = kin_beam.subsurface((45, 55), (42, 181))
kin_beam_rings = kin_beam.subsurface((45, 15), (42, 42))
kin_beam_impact = kin_beam.subsurface((45, 0), (42, 15))

#END beams

#START rays

#constants
v0_scalar = 2
accel_scalar = 1.15

single_growth_delay = 8
s_grwth_fctr_y = 4
s_grwth_fctr_x = 2

double_growth_delay = 16
d_grwth_fctr_y = 8
d_grwth_fctr_x = 6

#images
all_rays = pygame.image.load('projectiles\simple_rays.png').convert_alpha()
hot_rays = all_rays.subsurface((0,0),(56, 18))
cold_rays = all_rays.subsurface((0,19),(56, 18))
acid_rays = all_rays.subsurface((0,38),(56, 18))

hot_ray_1 = hot_rays.subsurface((0,0), (18, 18))

cold_ray_1 = cold_rays.subsurface((0,0), (18, 18))

#END rays

'''
class actor(entity):
def __init__(self, pos, img, size):
   super().__init__(pos, img.subsurface((0,0), size))
   self.velocity = (0, 0)
'''
'''
projectiles/missiles/spells are designed to be modular creations that can be mixed and matched 
to create new spells on the fly/custom build your ideal spell in the hub room
'''


class missile(spritelings.actor):
    def __init__(self, caster, img):
        super().__init__(img, caster.get_pos(1))

        self.damage = 0
        self.temp = 0
        self.knockback = (0,0)



#most basic missile/projectile. A small circle/square that travels out and hits things.
class bolt(missile):
    def __init__(self, caster, img, vel):
        super().__init__(caster, img)
        self.damage = 10
        xVel = vel[0] * 10
        yVel = vel[1] * 10
        self.velocity = (xVel, yVel)

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
        super().__init__(caster, kin_bolt, vel)

        xVel = vel[0] *14
        yVel = vel[1] *14
        self.velocity = (xVel, yVel)
        caster.cooldown += 15
        xk = self.velocity[0]/7
        yk = self.velocity[1]/7
        self.knockback = (xk, yk)


class fire_bolt(bolt):
    def __init__(self, caster, vel):
        super().__init__(caster, fire_ball_m, vel)

        caster.cooldown += 30
        xk = self.velocity[0] / 10
        yk = self.velocity[1] / 10
        self.knockback = (xk, yk)


class ice_bolt(bolt):
    def __init__(self, caster, vel):
        super().__init__(caster, ice_disc_m, vel)

        caster.cooldown += 30
        xk = self.velocity[0] / 10
        yk = self.velocity[1] / 10
        self.knockback = (xk, yk)


class acid_bolt(bolt):
    def __init__(self, caster, vel):
        super().__init__(caster, acid_orb_m, vel)

        caster.cooldown += 30
        xk = self.velocity[0] / 10
        yk = self.velocity[1] / 10
        self.knockback = (xk, yk)


#exploding projectile
class blast(missile):
    pass

#basically a helper class for the blast class. used to represent the smaller projectiles that split off from the main explosion
class frag(missile):
    pass


#beam and its subclasses might be unique enough to consider adding a special
#spritegroup to each room, just to handle beams and rays, as they will prbly
#require multiple sprites working in tandem
#instantaneous straight line laser attack
class beam(missile):
    def __init__(self, caster, img):
        super().__init__(caster, img)
        self.delay = beam_delay
        self.caster = caster


    def update(self):
        if self.delay > 0:
            self.delay -= 1
            self.rect.move_ip(self.caster.velocity)
            #charging cycle

        else:
            pass


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


#rays are a subclass of beams that can be heat or freeze. basically a coninuous stream of
#(purely) elemental damage
#currrently, basically everything is handled in the parent class ray, seeing as the only major difference between the 2
#types of ray is hot or cold, which boils down to a variable
class ray(beam):
    def __init__(self, caster, img, vel):
        super().__init__(caster, img)
        xVel = vel[0] * v0_scalar
        yVel = vel[1] * v0_scalar
        self.velocity = (xVel, yVel)
        self.timer = 0
        self.caster = caster
        self.mask = pygame.mask.from_surface(self.image, 0)

    def update(self):
        self.timer+=1
        self.rect.move_ip(self.velocity)
        #not sure how necessary this little bit here is, as it just adjusts the projectiles to match the movement/position
        #of the player/caster, to give the appearance of a single ray of heat
        self.rect.move_ip(self.caster.velocity)
        self.pos = (self.rect.x, self.rect.y)

        #problem here is getting the velocity to scale properly. I want the projectiles to enlarge as they travel
        #giving the appearance of a widening cone of heat, and they should accelerate as they travel,
        #to minimize overlap between each projectile. not sure how to handle this tho.
        #so far, i think this works well. It does appear to be VERY processor intensive
        #it may be worth it to add in a special sprite group JUST for handling rays, as they seem to slow down the game
        #all by themselves, so I shudder to think of what happens when we have them + anything else
        if(self.timer%single_growth_delay == 0):
            #I'm pretty sure its this part (the image scaling) thats causing the slow-downs. Let's consider pre-loading some or all of this
            self.set_image(pygame.transform.scale(self.image, (self.rect.width + s_grwth_fctr_x, self.rect.height + s_grwth_fctr_y)))
            self.rect.move_ip(0,-(s_grwth_fctr_y/2))
            xVel = self.velocity[0] * accel_scalar
            yVel = self.velocity[1] * accel_scalar
            self.velocity = (xVel, yVel)
        if (self.timer % double_growth_delay == 0):
            self.set_image(pygame.transform.scale(self.image, (self.rect.width + d_grwth_fctr_x, self.rect.height + d_grwth_fctr_y)))
            self.rect.move_ip(0, -(d_grwth_fctr_y/2))


    def act(self, target):
        target.react(self)
        self.kill()

    def act(self, target_list):
        for target in target_list:
            target.react(self)
            self.kill()

class heat_ray(ray):
    def __init__(self, caster, vel):
        super().__init__(caster, hot_ray_1, vel)


class freeze_ray(ray):
    def __init__(self, caster, vel):
        super().__init__(caster, cold_ray_1, vel)

#short-range, conical shotgun spread
class burst(missile):
    pass



class barrier(missile):
    pass