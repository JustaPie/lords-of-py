import pygame
import spritelings
import math


class enemy(spritelings.actor):
    def __init__(self, img, pos):
        super().__init__(img, pos)
        self.speed = 0
        self.acc = 0
        self.damage = 0
        self.cold_threshold = -100
        self.temp = 0
        self.heat_threshold = 150


    # handler method for sequencing move orders, calculating movement vectors,
    # picking and checking locations,
    def movement(self, pattern):
        pass


    # the following vector methods have to do with adjusting
    # position, velocity, and acceleration
    def dumb_move(self, target):
        dx, dy = self.rect.x - target.rect.x, self.rect.y - target.rect.y
        dist = math.hypot(dx, dy)
        xvel = self.velocity[0] * dx / dist
        yvel = self.velocity[1] * dy / dist
        self.velocity = (xvel, yvel)


    def move_to_sprite(self, target):
        dx, dy = self.rect.x - target.rect.x, self.rect.y - target.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        self.velocity = (self.rect.x + dx * self.speed,
                         self.rect.y + dy * self.speed)


    def react(self, weapon):
        self.hp -= weapon.damage
        self.rect.move_ip(weapon.knockback)
        self.temp += weapon.temp
        if self.state == 'normal':
            if self.temp < self.cold_threshold:
                self.state = 'frozen'

            elif self.temp > self.heat_threshold:
                self.state = 'burning'


    def act(self, victim):
        victim.react(self)


    def act(self, victim_list):
        for victim in victim_list:
            victim.react(self)

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

    def check_state(self):
        if self.temp < 0:
            self.temp += 1
            if self.temp < self.cold_threshold:
                self.state = 'frozen'
                self.velocity = (0,0)
        elif self.temp > 0:
            self.temp -= 1
            if self.temp > self.heat_threshold:
                self.state = 'burning'

        if self.state == 'frozen':
            self.velocity = (0, 0)
            if self.temp >=0:
                self.state = 'normal'

        if self.state == 'burning':
            self.hp -= 15

