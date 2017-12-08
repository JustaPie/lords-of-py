import random

import pygame

import spritelings

#####################################################
#############   OVERLAYS    #########################
#####################################################
# overlays are a mostly cosmetic effects class for drawing an image to the screen on top of something. Adding overlays
# to a sprite is a handy way of managing recurring images within the sprite to which they apply. this might also be our
# go-to way of printing text to the screen. Its also how I handle healthbars, for the player and potentially enemies

blank = pygame.image.load('people\hud_blank.png').convert_alpha()
#blank.set_colorkey((255, 255, 255))
bar = pygame.image.load('overlays\hpbar.png').convert_alpha()
hp_bar = bar.subsurface((0,0), (600, 30))
empty_bar = bar.subsurface((0, 31), (600, 30))

class healthbar(spritelings.overlay):
    def __init__(self, subject, master = None):
        super().__init__(hp_bar, subject.rect.center)
        self.master = master
        self.subject = subject

    def update(self, *args):
        self.image = bar.subsurface((0,0), (self.subject.hp, 30))
        self.rect.center = self.subject.rect.center
        self.rect.bottom = self.subject.rect.top



class focusbar(spritelings.overlay):
    pass

class magic_book(spritelings.overlay):
    pass

class hud_plate(spritelings.overlay):
    pass

class hud(pygame.sprite.Group):
    def __init__(self, player, display, *args):
        super().__init__(*args)
        self.hp = healthbar(player)
        self.subject = player
        self.add(self.hp)
        self.display = display
        self.rect = display.get_rect()

    def update(self, room):
        self.hp.update()
        self.draw(self.display)

    def draw(self, *args):
        self.display.blit(empty_bar, (0, 0))
        self.display.blit(self.hp.image, (0, 0))


eye_chart = pygame.image.load('baddies\eye_chart.png').convert_alpha()
neutral = eye_chart.subsurface((64, 64), (65, 65))
bottom = eye_chart.subsurface((64,128), (65, 65))
top = eye_chart.subsurface((64,0), (65, 65))
left = eye_chart.subsurface((0,64), (65, 65))
right = eye_chart.subsurface((128,64), (65, 65))
top_right = eye_chart.subsurface((128,0), (65, 65))
top_left = eye_chart.subsurface((0,0), (65, 65))
bottom_left = eye_chart.subsurface((0,128), (65, 65))
bottom_right = eye_chart.subsurface((128, 128), (65, 65))

class eyeball(spritelings.overlay):
    def __init__(self, subject, room, scale=64):
        super().__init__(neutral, subject.rect.center)
        self.subject = subject
        size = (int(scale*.35), int(scale*.35))
        fix = pygame.transform.scale
        self.eye_lookup = {(0, 0): fix(neutral, size), (1, 0): fix(right, size), (1, -1): fix(top_right, size),
                           (1, 1): fix(bottom_right, size),(0, -1): fix(top, size), (0, 1): fix(bottom, size),
                           (-1, 0): fix(left, size), (-1, -1): fix(top_left, size), (-1, 1): fix(bottom_left, size)}
        self.rect.center = self.subject.rect.center
        self.image = self.eye_lookup[self.subject.facing]
        room.nme_overlays.add(self)

    def update(self, room):
        self.image = self.eye_lookup[self.subject.facing]
        self.rect.center = self.subject.rect.center

ice_cube = pygame.image.load('overlays\generic_ice_cube.png')
idle_flame = pygame.image.load('projectiles\simple_missiles.png').convert_alpha()

class status_layer(pygame.sprite.Group):
    def __init__(self, subject,  *args):
        super().__init__(*args)
        self.subject = subject

class ice_sprite(spritelings.overlay):
    def __init__(self, subject):
        super().__init__(ice_cube, subject.rect.center)
        print('something should be frozen')
        self.subject = subject

    def update(self, room):
        self.rect.center = self.subject.rect.center
        #room.overlays.add(self)

class fire_sprite_cluster(pygame.sprite.Group):
    def __init__(self, subject, *args):
        super().__init__(*args)
        self.subject = subject
        for x in range(5):
            self.add(fire_sprite(self.subject))

class fire_sprite(spritelings.overlay):
    def __init__(self, subject):
        super().__init__(idle_flame, subject.rect.center)
        self.image_lookup = {0: idle_flame.subsurface((54, 69), (11, 35)),
                             1: idle_flame.subsurface((43, 76), (9, 27)),
                             2: idle_flame.subsurface((29, 71), (11, 33)),
                             3: idle_flame.subsurface((16, 77), (11, 26)),
                             4: idle_flame.subsurface((4, 71), (9, 32))}
        self.subject = subject
        from random import randint
        self.count = randint(0,4)
        self.image = self.image_lookup[self.count]
        self.rect = self.image.get_rect()
        self.rect.center = (randint(0, subject.rect.width, randint(0, subject.rect.height)))

    def update(self, room):
        center = self.rect.center
        if self.count < 4:
            self.count+=1
        elif self.count == 4:
            self.count = 0
        self.image = self.image_lookup[self.count]
        self.rect = self.image.get_rect()
        self.rect.center = center


class acid_sprite(spritelings.overlay):
    def __init__(self, subject):
        super().__init__(pygame.transform.scale(ice_cube, (subject.rect.width, subject.rect.height)), subject.rect.center)
        self.subject = subject

    def update(self, room):
        self.rect.center = self.subject.rect.center
        #room.overlays.add(self)

impacts = pygame.image.load('overlays\impacts.png').convert_alpha()
standard_impact = impacts.subsurface((2,2), (128, 128))
hot_impact = impacts.subsurface((130,1), (128, 128))
chill_impact = impacts.subsurface((261, 1), (128, 128))
splat_impact = impacts.subsurface((392, 1), (128, 128))

class impact(spritelings.overlay):
    def __init__(self, img,  pos, variance = 8):
        x, y = pos[0] + random.randint(-variance, variance), pos[1] + random.randint(-variance, variance)
        super().__init__(img, (x,y))
        self.timer = 6

    def update(self, room):
        super().update(room)
        if self.timer <= 0:
            self.kill()
        self.timer -= 1

class generic_impact(impact):
    def __init__(self, pos, size = 16):
        super().__init__(pygame.transform.scale(standard_impact, (size, size)), pos)


class fiery_impact(impact):
    def __init__(self, pos, size = 16):
        size += random.randint(size/2, size)
        super().__init__(pygame.transform.scale(hot_impact, (size, size)), pos)

class cold_impact(impact):
    def __init__(self, pos, size=8):
        super().__init__(pygame.transform.scale(chill_impact, (size, size)), pos)
        self.timer = 0

    def update(self, room):
        self.timer+=1
        if self.timer >= 16:
            self.kill()
        self.image = pygame.transform.scale(chill_impact, (self.rect.width+self.timer, self.rect.height+self.timer))

class acid_impact(impact):
    def __init__(self, pos, size=8):
        super().__init__(pygame.transform.scale(splat_impact, (size, size)), pos)
        self.timer = 16
