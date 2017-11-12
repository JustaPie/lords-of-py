import pygame
import spritelings


def __init__(self, img, pos):
    super().__init__(img, pos)
    self.speed = 0
    self.acc = 0
    self.damage = 0


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


def act(self, victim):
    victim.hp -= 10
    victim.velocity = self.velocity


def act(self, victim_list):
    for victim in victim_list:
        victim.hp -= self.damage
        victim.velocity = self.velocity


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
    print(self.velocity)


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
