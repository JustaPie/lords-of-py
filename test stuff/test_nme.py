import pygame
import spritelings
import missiles
import room
import random

vmax = 14
acc = 14

wing_eye = pygame.image.load('baddies\wing_eye.png').convert_alpha()

class fleye(spritelings.enemy):
    def __init__(self, pos):
        super().__init__(self, wing_eye, pos)

        self.hp = 100
        self.damage = 10
        self.dest = self.pos
        self.pos_vector = (0, 0)
        self.vel_vector = (0, 0)
        self.acc_vector = (0, 0)
        self.timer = 0

    def update(self, room):
        self.timer += 1
        if self.timer % 28 == 0:
            self.timer = 0
            self.get_pos_vector()
            self.get_vel_vector()
        self.get_acc_vector()


    def movement(self):
        pass

    def attack(self):
        pass

    def get_pos_vector(self):
        xdest = self.dest[0]
        ydest = self.dest[1]
        xpos = self.pos[0]
        ypos = self.pos[1]
        dx = xpos - xdest
        dy = ypos - ydest
        self.pos_vector = (dx, dy)
        return (dx, dy)

    def get_vel_vector(self):
        dx = self.pos_vector[0]
        dy = self.pos_vector[1]
        if dx > dy:
            vmult = round(dx/vmax, 0)
            yvel = vmax/vmult
            if dx >= vmax:
                xvel = vmax
            else:
                xvel =  dx

        elif dy > dx:
            vmult = round(dy/vmax, 0)
            xvel = vmax / vmult
            if dy >= vmax:
                yvel = vmax
            else:
                yvel = dx

        else:
            if vmax < dx:
                xvel = vmax
                yvel = vmax

            else:
                xvel = dx
                yvel = dy
        self.vel_vector = (xvel, yvel)
        return (xvel, yvel)


    def get_acc_vector(self):
        xvel = self.velocity[0]
        yvel = self.velocity[1]
        if self.velocity[0] < self.vel_vector[0]:
            xvel += acc
        if self.velocity[1] < self.vel_vector[1]:
            yvel += acc
        self.velocity = (xvel, yvel)
