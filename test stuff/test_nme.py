import pygame
import spritelings
import missiles
import room
import random
import enemies


winged_eye = pygame.image.load("baddies\winged_eye2.png").convert_alpha()
winged_eye_back = winged_eye.subsurface((1, 1), (234, 116))
winged_eye_front = winged_eye.subsurface((236, 1), (233, 116))
#winged_eye_damaged = pygame.image.load("baddies\winged_eye_damaged.png").convert_alpha()
winged_eye_burning = winged_eye.subsurface((563, 135), (227, 169))
winged_eye_frozen = winged_eye.subsurface((564, 9), (232, 124))
winged_eye_acid = winged_eye.subsurface((865, 12), (216, 124))
winged_eye_impact = winged_eye.subsurface((245, 314), (227, 150))

fleye_img_lookup = {'normal': winged_eye_front, 'burning': winged_eye_burning, 'frozen': winged_eye_frozen}

class fleye(enemies.enemy):
    def __init__(self, pos):
        super().__init__(winged_eye_front, pos)

        self.hp = 100
        self.damage = 10
        self.dest = self.pos
        self.acc = .1
        self.timer = 0
        self.target = None
        self.state = 'normal'
        self.cold_threshold = -100
        self.temp = 0
        self.heat_threshold = 150

    def update(self, room):
        if self.target:
            print("fleye's target: ", self.target)
            self.accel_to_sprite(self.target)
        print("fleye's velocity: ", self.velocity)
        self.check_state()
        self.set_image(fleye_img_lookup[self.state])
        self.rect.move_ip(self.velocity)
        self.pos = (self.rect.x, self.rect.y)


    def set_target(self, target):
        self.target = target


