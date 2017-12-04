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
        #print('calling cond_queue')
        for eff in self.internals:
            print('eff = ', eff, type(eff))
            if not eff(self.subject):
                self.internals.remove(eff)

    def add(self, cond):
        matched = False
        for curr in self.internals:
           if curr.match == cond.match:
               curr.extend(cond)
               matched = True
        if not matched:
            self.internals.append(cond)



class entity(pygame.sprite.Sprite):
    def __init__(self, img, pos):
        super().__init__()
        self.image = img
        self.rect = img.get_rect()
        self.rect.center = pos
        self.hitbox = self.rect
        self.effects = []

        self.velocity = (0,0)
        self.knockback = (0,0)
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

    def apply(self, effects):
        for effect in effects:
            self.condition.add(effect)

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
