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


class player(entity):
    def __init__(self, img, pos):
        super().__init__(img, pos)


class enemy(entity):
    def __init__(self, img, pos):
        super().__init__(img, pos)


class missile(entity):
    def __init__(self, img, pos):
        super().__init__(img, pos)


class block(entity):
    def __init__(self, img, pos):
        super().__init__(img, pos)

