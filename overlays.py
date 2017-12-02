import pygame
import spritelings
import player

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
    def __init__(self, subject, master):
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
        self.hp = healthbar(player, self)
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
    def __init__(self, subject, room):
        super().__init__(neutral, subject.rect.center)
        self.subject = subject
        self.eye_lookup = {(0, 0): neutral, (1, 0): right, (1, -1): top_right, (1, 1): bottom_right,
         (0, -1): top, (0, 1): bottom, (-1, 0): left, (-1, -1): top_left, (-1, 1): bottom_left}
        self.rect.center = self.subject.rect.center
        self.image = self.eye_lookup[self.subject.facing]
        room.nme_overlays.add(self)

    def update(self, room):
        self.image = self.eye_lookup[self.subject.facing]
        self.rect.center = self.subject.rect.center

ice_cube = pygame.image.load('overlays\generic_ice_cube.png')

class frozen(spritelings.overlay):
    def __init__(self, subject):
        super().__init__(ice_cube, subject.rect.center)
        self.subject = subject


    def update(self, room):
        self.rect.center = self.subject.rect.center
        room.overlays.add(self)

class burning(spritelings.overlay):
    def __init__(self, subject):
        super().__init__(ice_cube, subject.rect.center)
        self.subject = subject


    def update(self, room):
        self.rect.center = self.subject.rect.center
        room.overlays.add(self)