import pygame
import spritelings
import math
import missiles


class enemy(spritelings.actor):
    def __init__(self, img, pos):
        super().__init__(img, pos)
        self.speed = 0
        self.acc = 0
        self.damage = 0
        self.spell = None
        self.state = 'normal'
        self.target = None


    def update(self, room):
        if self.target:
            self.facing = self.track(self.target)

    def set_target(self, target):
        self.target = target

    def react(self, weapon):
        self.hp -= weapon.damage
        self.rect.move_ip(weapon.knockback)
        self.temp += weapon.temp
        if self.state == 'normal':
            if self.temp < self.max_cold:
                self.state = 'frozen'

            elif self.temp > self.max_heat:
                self.state = 'burning'

    def act(self, victims):
        for victim in victims:
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

    #basic method to get an enemy to slow down until stopping
    def slow_to_stop(self):
        x, y = self.velocity
        if x < 0-self.acc:
            x += self.acc
        elif x > 0+self.acc:
            x -= self.acc
        else:
            x = 0

        if y < 0-self.acc:
            y += self.acc
        elif y > 0+self.acc:
            y -= self.acc
        else:
            y = 0
        self.velocity = (x, y)

    #mathematical (read: non-functional) method for making an enemy circle a target
    def circle(self, target):
        #sets the enemy to face the target, then it will pick a random direction
        #that is normal to the target's relative position, and then moves (sets velocity)
        #along that path. After moving for a bit, it sets itself to accel_to_sprite
        dir = self.track(target)



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
        self.timer = 128*20
        self.target = None
        self.state = 'normal'
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





bouncer_sheet = pygame.image.load('baddies\\bumper.png').convert_alpha()
bouncer_neutral = bouncer_sheet.subsurface((1,1), (181, 181))
bouncer_left = bouncer_sheet.subsurface((185, 1), (181, 181))
bouncer_top_left = bouncer_sheet.subsurface((373, 1),(181, 181))
bouncer_bottom_left = pygame.transform.flip(bouncer_top_left, 0, 1)
bouncer_right = pygame.transform.flip(bouncer_left, 1, 0)
bouncer_top_right = pygame.transform.flip(bouncer_top_left, 1, 0)
bouncer_bottom_right = pygame.transform.flip(bouncer_top_right, 0, 1)
bouncer_top = bouncer_sheet.subsurface((558, 0), (181, 181))
bouncer_bottom = pygame.transform.flip(bouncer_top, 0, 1)

class bouncer(enemy):
    def __init__(self, pos):
        super().__init__(bouncer_neutral, pos)

        self.lookup = {(0, 0): bouncer_neutral, (1, 0): bouncer_right, (1, -1): bouncer_top_right, (1, 1): bouncer_bottom_right,
         (0, -1): bouncer_top, (0, 1): bouncer_bottom, (-1, 0): bouncer_left, (-1, -1): bouncer_top_left, (-1, 1): bouncer_bottom_left}

        self.timer = 0
        self.spell = missiles.fire_bolt

    def look_at(self):
        self.image = self.lookup[self.facing]

    #@look_at
    def update(self, room):
        super().update(room)
        self.look_at()
        if self.timer > 0:
            self.timer -= 1
        else:
            self.spell.fire(self.spell(self), self.facing, room.enemyProjectiles)
            self.timer = 356





