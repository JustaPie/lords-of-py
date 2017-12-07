import pygame

import missiles
import overlays
import room
import spritelings


def slow(velocity, by):
    return velocity[0] - velocity[0]*by, velocity[1] - velocity[1]*by

class enemy(spritelings.actor):
    def __init__(self, img, pos):
        super().__init__(img, pos)
        self.speed = 0
        self.acc = 0
        self.damage = 10
        self.spell = None
        self.target = None
        self.hp = 300
        #self.overlays.add(overlays.healthbar(self))
        self.armor = .15
        self.hitboxes = [self.hitbox]
        #self.flash_image = overlays.generic_flash
        self.fire_sprite = overlays.fire_sprite
        self.ice_sprite = overlays.ice_sprite
        self.acid_sprite = overlays.acid_sprite


    def update(self, room):
        if self.hp<=0:
            self.kill()
        if not self.flashing:
            pass

        if self.target:
            self.facing = self.track(self.target)
        self.condition()
        room.overlays.add(self.overlays)
        self.rect.move_ip(self.velocity)
        self.hitbox.center = self.rect.center


    def set_target(self, target):
        self.target = target

    def react(self, weapon):
        self.hp -= weapon.damage
        weapon.velocity = slow(weapon.velocity, self.armor)
        self.rect.move_ip(weapon.knockback)
        '''
        if not self.flashing:
            self.flashing += 4
        elif self.flashing:
            self.overlays.add(self.flash_image(self.rect.center))
        '''


    def act(self, victims):
        for victim in victims:
            self.knockback = (-victim.velocity[0], -victim.velocity[1])
            victim.react(self)
            for effect in self.effects:
                effect(victim)


    def move_to(self, dest):
        xdest, ydest = dest[0], dest[1]
        xpos, ypos = self.rect.x, self.rect.y
        xvel, yvel = 0, 0
        dx, dy = xdest-xpos, ydest-ypos
        if xvel > dx:
            xvel = 1
        elif xvel < dx:
            xvel = 1
        else:
            xvel = 0
        if yvel > dy:
            yvel = -1
        elif yvel < dy:
            yvel = 1
        else:
            yvel = 0
        self.velocity = (xvel, yvel)


    def accel_to_sprite(self, target):
        xvel, yvel = self.velocity[0], self.velocity[1]
        xpos = self.rect.x
        ypos = self.rect.y
        xdest = target.rect.x
        ydest = target.rect.y
        if xpos < xdest:
            xvel += self.acc
        elif xpos > xdest:
            xvel -= self.acc
        else:
            pass
        if ypos < ydest:
            yvel += self.acc
        elif ypos > ydest:
            yvel -= self.acc
        else:
            pass

        self.velocity = (xvel, yvel)


    def accel_to_dest(self, dest):
        xvel, yvel = self.velocity[0], self.velocity[1]
        xpos = self.rect.x
        ypos = self.rect.y
        xdest = dest[0]
        ydest = dest[1]
        if xpos < xdest:
            xvel += self.acc
        elif xpos > xdest:
            xvel -= self.acc
        else:
            pass
        if ypos < ydest:
            yvel += self.acc
        elif ypos > ydest:
            yvel -= self.acc
        else:
            pass
        self.velocity = (xvel, yvel)

    #basic method to get an enemy to slow down until stopping
    def slow_to_stop(self):
        x, y = self.velocity
        if x < 0-self.acc:
            x += self.acc
        elif x > 0+self.acc:
            x -= self.acc
        else:
            x = 0

        if y < 0-self.acc:
            y += self.acc
        elif y > 0+self.acc:
            y -= self.acc
        else:
            y = 0
        self.velocity = (x, y)

    #mathematical (read: non-functional) method for making an enemy circle a target
    def circle(self, target):
        #sets the enemy to face the target, then it will pick a random direction
        #that is normal to the target's relative position, and then moves (sets velocity)
        #along that path. After moving for a bit, it sets itself to accel_to_sprite
        dir = self.track(target)



    def vel_to_sprite(self, target):
        xvel = self.velocity[0]
        yvel = self.velocity[1]
        xpos = self.rect.x
        ypos = self.rect.y
        xdest = target.rect.x
        ydest = target.rect.y
        if xpos < xdest:
            xvel += self.acc
        elif xpos > xdest:
            xvel -= self.acc
        else:
            pass
        if ypos < ydest:
            yvel += self.acc
        elif ypos > ydest:
            yvel -= self.acc
        else:
            pass
        self.velocity = (xvel, yvel)

loognoog = pygame.image.load('baddies\loogloog.png').convert_alpha()

class lugg(enemy):
    def __init__(self, pos):
        super().__init__(pygame.transform.scale(loognoog, (300,200)), pos)
        self.hp = 100000


#####################################################
#############   FLEYES      #########################
#####################################################
#bog standard flying enemies, they swoop wildly around, orbiting the player

winged_eye = pygame.image.load("baddies\winged_eye2.png").convert_alpha()
winged_eye_back = winged_eye.subsurface((1, 1), (234, 116))
winged_eye_front = winged_eye.subsurface((236, 1), (233, 116))
winged_eye_burning = winged_eye.subsurface((563, 135), (227, 169))
winged_eye_frozen = winged_eye.subsurface((564, 9), (232, 124))
winged_eye_acid = winged_eye.subsurface((865, 12), (216, 124))
winged_eye_impact = winged_eye.subsurface((245, 314), (227, 150))

fleye_img_lookup = {'normal': winged_eye_front, 'burning': winged_eye_burning, 'frozen': winged_eye_frozen}

feyenal_fleye = pygame.image.load("baddies\\feyenal_fleye.png").convert_alpha()

#just sorta flies around the player at semi-ridiculous speeds.
class fleye(enemy):
    def __init__(self, pos):
        super().__init__(feyenal_fleye, pos)
        self.hitbox = self.rect.inflate(-(self.rect.width*0.7), -(self.rect.height*0.5))
        self.hitbox.center = self.rect.center
        self.hp = 30
        self.damage = 10
        self.dest = self.rect.center
        self.acc = .2
        self.timer = 128*20
        self.target = None
        self.roost = self.rect.center
        self.roosting = 0
        self.eye = None
        self.hitboxes = [self.hitbox]

    def update(self, room):
        if self.hp <= 0:
            self.eye.kill()
            self.kill()

        if not self.eye:
            self.eye = overlays.eyeball(self, room)
        self.eye.update(room)

        self.timer -= 1

        if self.roosting:
            self.move_to(self.roost)
            self.timer += 1

            if self.timer >= 128*30:
                print('waking up')
                self.roosting = 0

        #if the timer isn't up, fleye chases the player
        elif self.target and self.timer > 0:
            self.accel_to_sprite(self.target)

        #runs a little timer that makes fleye chase the player for a bit, then go back to its starting position
        elif self.timer <= 0:
            print('going to bed')
            self.roosting = 1

        #self.check_state()
        self.rect.move_ip(self.velocity)
        self.hitbox.center = self.rect.center
        self.eye.rect.center = self.rect.center



#####################################################
#############   BOUNCERS    #########################
#####################################################
#the bouncer overclass contains several variants of bouncers.
#their thing is that they react to incoming sprites and walls
#by altering velocities

bouncer_sheet = pygame.image.load('baddies\\bumper.png').convert_alpha()
basic_bouncer_img = bouncer_sheet.subsurface((1,1), (181, 181))
blue_bouncer_img = bouncer_sheet.subsurface((185, 1), (181, 181))
black_bouncer_img = bouncer_sheet.subsurface((373, 1),(181, 181))
blind_bouncer_img = bouncer_sheet.subsurface((558, 0), (181, 181))
baby_bouncer_img = pygame.transform.scale(basic_bouncer_img, (64, 64))
ow = pygame.mixer.Sound("audio/ow.wav")

#standard version; bounces off walls and bullets, flying away from them on contact
class bouncer(enemy):
    def __init__(self, pos):
        super().__init__(basic_bouncer_img, pos)
        self.eye = None
        self.timer = 0
        self.spell = missiles.ice_bolt
        self.core = self.rect.inflate(-96, -96)
        self.top = pygame.Rect(*self.rect.center, 43, 43)

        self.bottom = pygame.Rect(*self.rect.center, 43, 43)

        self.left = pygame.Rect(*self.rect.center, 43, 43)

        self.right = pygame.Rect(*self.rect.center, 43, 43)

        self.hitboxes = [self.core, self.top, self.bottom, self.left, self.right]

    def update(self, room):
        super().update(room)
        self.right.midright = self.rect.midright
        self.left.midleft = self.rect.midleft
        self.top.midtop = self.rect.midtop
        self.bottom.midbottom = self.rect.midbottom
        self.core.center = self.rect.center

        if not self.eye:
            self.eye = overlays.eyeball(self, room)
        self.eye.update(room)

        if self.timer > 0:
            self.timer -= 1
        else:
            #sound effect
            self.spell.fire(self.spell(self), self.facing, room.enemyProjectiles)
            self.timer = 356

    def react(self, weapon):
        if pygame.Rect.colliderect(self.core, weapon.hitbox):
            self.hp -= weapon.damage
<<<<<<< HEAD
            ow.play()
            self.velocity = (self.velocity[0]*weapon.stopping_power, self.velocity[1]*weapon.stopping_power)
=======
>>>>>>> 5fd37743673fe686066d28113c92c47d6b3a32ea
    #so I'm handling missile penetration a bit weirdly here. All bullets travel at a given velocity, when it strikes a
    #enemy, the enemy slows the bullet, when velocity drops to a certain point, the bullet stops dealing damage
            if isinstance(weapon, missiles.missile):
                x = weapon.velocity[0]-weapon.velocity[0]*self.armor
                y = weapon.velocity[1]-weapon.velocity[1]*self.armor
                weapon.velocity = (x, y)
        if pygame.Rect.colliderect(self.bottom, weapon.hitbox):
            self.velocity = (self.velocity[0], -10)
            weapon.velocity = (0,0)
        if pygame.Rect.colliderect(self.left, weapon.hitbox):
            self.velocity = (10, self.velocity[1])
            weapon.velocity = (0, 0)
        if pygame.Rect.colliderect(self.top, weapon.hitbox):
            self.velocity = (self.velocity[0], 10)
            weapon.velocity = (0, 0)
        if pygame.Rect.colliderect(self.right, weapon.hitbox):
            self.velocity = (-10, self.velocity[1])
            weapon.velocity = (0, 0)

    def act(self, victims):
        for victim in victims:
            self.knockback = (-victim.velocity[0], -victim.velocity[1])
            if pygame.Rect.colliderect(self.core, victim.hitbox):
                victim.react(self)


#reacts to incoming fire by bouncing towards it
class blue_bouncer(bouncer):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = blue_bouncer_img

    def react(self, weapon):
        if pygame.Rect.colliderect(self.core, weapon.hitbox):
            self.hp -= weapon.damage
            #self.rect.move_ip(weapon.knockback)
            if isinstance(weapon, missiles.missile):
                weapon.velocity = (weapon.velocity[0]*self.armor, weapon.velocity[1]*self.armor)
        if pygame.Rect.colliderect(self.bottom, weapon.hitbox):
            if isinstance(weapon, room.wall):
                self.velocity = (self.velocity[0], -10)
            else:
                self.velocity = (self.velocity[0], 10)
                weapon.velocity = (0, 0)
        if pygame.Rect.colliderect(self.left, weapon.hitbox):
            if isinstance(weapon, room.wall):
                self.velocity = (10, self.velocity[1])
            else:
                self.velocity = (-10, self.velocity[1])
                weapon.velocity = (0, 0)
        if pygame.Rect.colliderect(self.top, weapon.hitbox):
            if isinstance(weapon, room.wall):
                self.velocity = (self.velocity[0], 10)
            else:
                self.velocity = (self.velocity[0], -10)
                weapon.velocity = (0, 0)
        if pygame.Rect.colliderect(self.right, weapon.hitbox):
            if isinstance(weapon, room.wall):
                self.velocity = (-10, self.velocity[1])
            else:
                self.velocity = (10, self.velocity[1])
                weapon.velocity = (0, 0)


#bounces incoming missiles back towards their origin
class black_bouncer(bouncer):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = black_bouncer_img
        self.reflected = pygame.sprite.Group()

    def react(self, weapon):
        if pygame.Rect.colliderect(self.bottom, weapon.hitbox):
            weapon.velocity = (-weapon.velocity[0], 10)
            self.reflected.add(weapon)
        elif pygame.Rect.colliderect(self.left, weapon.hitbox):
            weapon.velocity = (-10, -weapon.velocity[1])
            self.reflected.add(weapon)
        elif pygame.Rect.colliderect(self.top, weapon.hitbox):
            weapon.velocity = (-weapon.velocity[0], -10)
            self.reflected.add(weapon)
        elif pygame.Rect.colliderect(self.right, weapon.hitbox):
            weapon.velocity = (10, -weapon.velocity[1])
            self.reflected.add(weapon)

        elif pygame.Rect.colliderect(self.core, weapon.hitbox):
            self.hp -= weapon.damage
            #self.rect.move_ip(weapon.knockback)
            if isinstance(weapon, missiles.missile):
                weapon.velocity = (weapon.velocity[0]*self.armor, weapon.velocity[1]*self.armor)

    def update(self, room):
        super().update(room)
        room.enemyProjectiles.add(self.reflected)



#nearly the same as the basic bouncer, except it doesn't shoot
class blind_bouncer(bouncer):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = blind_bouncer_img
        self.eye = None

    def update(self, room):
        #super().update(room)
        if self.hp<=0:
            self.kill()
        if self.target:
            self.facing = self.track(self.target)
        self.rect.move_ip(self.velocity)
        self.hitbox.center = self.rect.center
        self.right.midright = self.rect.midright
        self.left.midleft = self.rect.midleft
        self.top.midtop = self.rect.midtop
        self.bottom.midbottom = self.rect.midbottom
        self.core.center = self.rect.center


#extra small version of the basic bouncer designed to be spawned in swarms that fly erratically around the room,
#bouncing off of each other
class baby_bouncer(bouncer):
    pass




'''         if pygame.Rect.colliderect(self.bottom, victim.hitbox):
                self.velocity = (self.velocity[0], -10)
            if pygame.Rect.colliderect(self.left, victim.hitbox):
                self.velocity = (10, self.velocity[1])
            if pygame.Rect.colliderect(self.top, victim.hitbox):
                self.velocity = (self.velocity[0], 10)
            if pygame.Rect.colliderect(self.right, victim.hitbox):
                self.velocity = (-10, self.velocity[1])'''

