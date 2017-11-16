import pygame

def collide_hitbox(spriteA, spriteB):
    return pygame.Rect.colliderect(spriteA.hitbox, spriteB.hitbox)

class entity(pygame.sprite.Sprite):
    def __init__(self, img, pos):
        super().__init__()
        self.image = img
        self.rect = img.get_rect()
        self.rect.center = pos
        self.hitbox = self.rect
        self.velocity = (0,0)

        self.state = 'normal'
        self.temp = 0
        self.max_heat = 100
        self.max_cold = -100
        self.hp = 1000

    def set_size(self, size):
        pass

    def act(self, target):
        pass

    def react(self, bastard):
        pass

    def update(self, room):
        pass

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
