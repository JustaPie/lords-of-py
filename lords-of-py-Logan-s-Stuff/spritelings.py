import pygame

def collide_hitbox(spriteA, spriteB):
    if pygame.Rect.colliderect(spriteA.hitbox, spriteB.hitbox):
        for x in spriteB.hitboxes:
            if pygame.Rect.colliderect(spriteA.hitbox, x):
                return True
    else:
        return False


class cond_queue(object):
    def __init__(self, subject, *args):
        self.size = 0
        self.subject = subject
        self.internals = []
        for arg in args:
            self.internals.append(arg)
            self.size += 1

    def __call__(self):
        #print('calling cond_queue on: ', self.internals)
        for eff in self.internals:
            print('eff = ', eff, type(eff))
            result = eff(self.subject)
            if not result:
                self.internals.remove(eff)

    def add(self, cond):
        print('adding condition')
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
        self.hitboxes = [self.hitbox]

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

        self.skip = False

    def apply(self, *args):
        for arg in args:
            self.condition.add(arg)

    def set_size(self, size):
        pass

    def act(self, target):
        pass

    def react(self, bastard):
        pass

    def update(self, room):
        pass

class blank(pygame.sprite.Sprite):
    def __init__(self, *args):
        pass

class actor(entity):
    def __init__(self, img, pos):
        super().__init__(img, pos)
        self.facing = (0,0)
        self.cast_from = self.rect.center
        self.damage = 0
        self.flashing = 0
        self.fire_sprite = blank
        self.ice_sprite = blank
        self.acid_sprite = blank


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

    class burning(object):
        def __init__(self, duration):
            #super().__init__()
            self.match = 'burning'
            self.duration = duration
            self.ignited = False
            self.layer = None

        def __call__(self, target):
            from random import  randint
            if not self.ignited:
                self.layer = target.fire_sprite(target)
                target.overlays.add(self.layer)
                self.ignited = True
            target.hp -= randint(0, 1)
            self.duration -= 1
            if self.duration <= 0:
                target.overlays.remove(self.layer)
                return False
            else:
                return True

        def extend(self, blah):
            pass

    class frozen(object):
        def __init__(self, duration):
            self.duration = duration
            self.cubed = False
            self.match = 'frozen'
            self.layer = None

        def __call__(self, target):
            if not self.cubed:
                self.layer = target.ice_sprite(target)
                target.overlays.add(self.layer)
                self.cubed = True
            target.skip = True
            self.duration -=1
            if self.duration <= 0:
                target.overlays.remove(self.layer)
                return False
            else:
                return True

        def extend(self, blah):
            pass

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
