import pygame
import spritelings
import missiles
import room
import random

vmax = 14
acc = 14

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
        self.target = room.player[0]

    def update(self, room):

        self.rect.move_ip(self.velocity)
        self.pos = (self.rect.x, self.rect.y)


    def movement(self):
        pass

    def attack(self):
        pass

    def accel_towards_sprite(self, target):
        xvel, yvel = self.velocity[0], self.velocity[1]
        xpos = self.rect.x
        ypos = self.rect.y
        xdest = target.rect.x
        ydest = target.rect.y
        if abs(xvel) < vmax:
            if xpos < xdest:
                xvel -= acc
            elif xpos>xdest:
                xvel += acc
            else:
                pass
        if abs(yvel) < vmax:
            if ypos < ydest:
                yvel -= acc
            elif ypos > ydest:
                yvel += acc
            else:
                pass




    def get_pos_vector(self):
        xdest = self.dest[0]
        ydest = self.dest[1]
        xpos = self.pos[0]
        ypos = self.pos[1]
        dx = xdest - xpos
        dy = ydest - ypos
        self.pos_vector = (dx, dy)
        return (dx, dy)

    def get_vel_vector(self):
        dx = self.pos_vector[0]
        dy = self.pos_vector[1]
        if dx > dy:
            vmult = round(dx/vmax, 0)
            yvel = vmax/max(vmult, 1)
            if dx >= vmax:
                xvel = vmax
            else:
                xvel =  dx

        elif dy > dx:
            vmult = round(dy/vmax, 0)
            xvel = vmax/max(vmult, 1)
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
        if self.vel_vector[1] < 0:
            if xvel >= self.vel_vector[0]:
                if abs(xvel + acc) <= abs(vmax):
                    xvel = vmax
                elif abs(xvel + acc) > abs(vmax):
                    xvel += acc

        elif self.vel_vector[1] > 0:
            if xvel <= self.vel_vector[0]:
                if abs(xvel - acc) >= abs(vmax):
                    xvel = -vmax
                elif abs(xvel - acc) < abs(vmax):
                    xvel -= acc
        else:
            pass

        if self.vel_vector[1] < 0:
            if yvel >= self.vel_vector[1]:
                if abs(yvel + acc) <= abs(vmax) :
                    yvel = -vmax
                elif abs(yvel + acc) > abs(vmax) :
                    yvel += acc

        elif self.vel_vector[1] > 0:
            if yvel <= self.vel_vector[1]:
                if abs(yvel - acc) >= abs(vmax) :
                    yvel = vmax
                elif abs(yvel - acc) < abs(vmax):
                    yvel -= acc
        else:
            pass

        self.velocity = (xvel, yvel)
        print(self.velocity)
