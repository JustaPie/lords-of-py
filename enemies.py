import pygame
import spritelings
import math


class enemy(spritelings.entity):
    def __init__(self, img, pos):
        super().__init__(img, pos)
        self.speed = 0
        self.acc = 0
        self.damage = 0


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



winged_eye = pygame.image.load("baddies\winged_eye2.png").convert_alpha()
winged_eye_back = winged_eye.subsurface((1, 1), (234, 116))
winged_eye_front = winged_eye.subsurface((236, 1), (233, 116))
winged_eye_burning = winged_eye.subsurface((563, 135), (227, 169))
winged_eye_frozen = winged_eye.subsurface((564, 9), (232, 124))
winged_eye_acid = winged_eye.subsurface((865, 12), (216, 124))
winged_eye_impact = winged_eye.subsurface((245, 314), (227, 150))

fleye_img_lookup = {'normal': winged_eye_front, 'burning': winged_eye_burning, 'frozen': winged_eye_frozen}


class fleye(enemy):
    def __init__(self, pos):
        super().__init__(winged_eye_front, pos)

        self.hp = 30
        self.damage = 10
        self.dest = self.rect.center
        self.acc = .35
        self.timer = 128*3
        self.target = None
        self.state = 'normal'
        self.cold_threshold = -100
        self.temp = 0
        self.heat_threshold = 150
        self.roost = self.rect.center
        self.roosting = 0

    def update(self, room):
        if self.hp < 0:
            self.kill()
        self.timer -= 1

        if self.roosting:
            self.move_to(self.roost)
            self.timer += 1

            if self.timer >= 128*30:
                print('waking up')
                self.roosting = 0

        #if the timer isn't up, fleye chases the player
        elif self.target and self.timer > 0:
            self.accel_to_sprite(self.target)

        #runs a little timer that makes fleye chase the player for a bit, then go back to its starting position
        elif self.timer <= 0:
            print('going to bed')
            self.roosting = 1

        #self.check_state()
        self.rect.move_ip(self.velocity)



    def set_target(self, target):
        self.target = target


