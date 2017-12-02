import pygame

def collide_hitbox(spriteA, spriteB):
    if pygame.Rect.colliderect(spriteA.hitbox, spriteB.hitbox):
        for x in spriteB.hitboxes:
            if pygame.Rect.colliderect(spriteA.hitbox, x):
                return True
    else:
        return False
'''
def burn(me, magnitude, duration):
    pass

def melt(me, magnitude, duration):
    pass

def freeze(me, magnitude, duration):
    pass

def flash(me, duration):
    pass

def stagger(me, duration):
    pass
'''

class cond_queue(object):
    def __init__(self, subject, *args):
        self.size = 0
        self.subject = subject
        self.internals = []
        for arg in args:
            self.internals.append(arg)
            self.size += 1

    def __call__(self):
        for eff in self.internals:
            eff(self.subject)
            if eff == None:
                self.internals.remove(eff)

    def apply(self, cond, *args):
        for conds in self.internals:
            if cond.isinstance(conds):
                conds.extend(*args)
            else:
                self.internals.append(cond(*args))


class entity(pygame.sprite.Sprite):
    def __init__(self, img, pos):
        super().__init__()
        self.image = img
        self.rect = img.get_rect()
        self.rect.center = pos
        self.hitbox = self.rect


        self.velocity = (0,0)
        self.knockback = (0,0)

        self.state = 'normal'

        #eventual replacement for the state variable. this will contain a list of functions/functors that will be performed on the sprite during the update
        self.condition = cond_queue(self)
        self.overlays = pygame.sprite.Group()
        self.temp = 0
        self.max_heat = 100
        self.max_cold = -100
        self.hp = 1000
    #resistance is how well the subject resists being pierced by projectiles. Every frame, the subject subtracts this value from
    # the velocity of any hostile projectile in contact with it.
        self.resistance = (1, 1)

    def set_size(self, size):
        pass

    def act(self, target):
        pass

    def react(self, bastard):
        pass

    def update(self, room):
        pass

    #to be phased out and replaced with the conditions  mechanic
    def check_state(self):
        if self.temp < 0:
            self.temp += 1
            if self.temp < self.max_cold:
                self.state = 'frozen'
                self.velocity = (0,0)
        elif self.temp > 0:
            self.temp -= 1
            if self.temp > self.max_heat:
                self.state = 'burning'

        if self.state == 'frozen':
            self.velocity = (0, 0)
            if self.temp >=0:
                self.state = 'normal'

        if self.state == 'burning':
            self.hp -= 15


class actor(entity):
    def __init__(self, img, pos):
        super().__init__(img, pos)
        self.facing = (0,0)
        self.cast_from = self.rect.center
        self.damage = 0

    #simple, inheritable function designed to allow both the player and enemies to auto-track a target
    def track(self, target):
        x1, y1 = self.rect.x, self.rect.y
        x2, y2 = self.rect.x + self.rect.width, self.rect.y + self.rect.height
        targ = target.rect.center
        x0, y0 = 0, 0
        if targ[0] > x2:
            x0 = 1
        elif targ[0] < x1:
            x0 = -1

        if targ[1] < y1:
            y0 = -1
        elif targ[1] > y2:
            y0 = 1

        self.facing = (x0, y0)
        return (x0, y0)

    #a default version of the cast method from the player class, to be modified by sub-classes
    def cast(self, room):
        self.spell.fire(self.facing, room)

#im trying to do these as nested classes so we can re-define them for individual classes of enemies. That way, we can
# get different behaviors for different enemies
    class burn(object):
        def __init__(self, magnitude, duration):
            self.magnitude = magnitude
            self.duration = duration

        def __call__(self, subject):
            subject.hp -= self.magnitude
            self.duration -= 1
            if self.duration <= 0:
                self = None

        def extend(self, mag, dur):
            self.magnitude += mag
            self.duration += dur

    def melt(self, magnitude, duration):
        pass

    class freeze(object):
        def __init__(self, subject, magnitude):
            self.magnitude = magnitude
            self.duration = 128*3
            self.subject = subject

        def __call__(self, room):
            subject = self.subject
            freeze_factor = (self.magnitude - abs(subject.max_cold)) / abs(subject.max_cold)
            if freeze_factor >=1:
                subject.velocity = 0
                room.overlays.add(subject.frozen())
            x = subject.velocity[0]
            y = subject.velocity[1]
            x = x*freeze_factor
            y = y*freeze_factor
            subject.velocity = (x, y)
            self.duration = 128*10


            self.duration -= 1
            if self.duration <= 0:
                self.magnitude = 0
                return False
            return True

        def extend(self, mag):
            self.magnitude += mag
            if self.duration< 128*3:
                self.duration = 128*3


    def flash(self, duration):
        pass

    def stagger(self, duration):
        pass

    def affect(self, cond):
        self.condition.apply(cond)

class player(actor):
    def __init__(self, img, pos):
        super().__init__(img, pos)


class enemy(actor):
    def __init__(self, img, pos):
        super().__init__(img, pos)


class missile(entity):
    def __init__(self, img, pos):
        super().__init__(img, pos)


class block(entity):
    def __init__(self, img, pos):
        super().__init__(img, pos)

class overlay(entity):
    def __init__(self, img, pos):
        super().__init__(img, pos)
