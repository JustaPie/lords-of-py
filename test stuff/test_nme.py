import pygame
import spritelings
import missiles
import room
import random

acc = 2

winged_eye = pygame.image.load("baddies\wing_eye.png").convert_alpha()
wing_eye = winged_eye.subsurface((6, 18), (160, 58))

class fleye(spritelings.enemy):
    def __init__(self, pos):
        super().__init__(wing_eye, pos)

        self.hp = 100
        self.damage = 10
        self.dest = self.pos
        self.pos_vector = (0, 0)
        self.vel_vector = (0, 0)
        self.acc_vector = (0, 0)
        self.timer = 0
        self.target = None
        self.set_image(pygame.transform.scale(self.image, (80, 29)))

    def update(self, room):
        if self.target:
            self.accel_towards_sprite()
        self.rect.move_ip(self.velocity)
        self.pos = (self.rect.x, self.rect.y)

    def set_target(self, target):
        self.target = target


