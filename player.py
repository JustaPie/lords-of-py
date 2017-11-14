import pygame
import spritelings
import missiles
import controller
import keyboard
import keyboard_alt

pc_pict = pygame.image.load('people\grn_plyr_arw.png').convert_alpha()
speed = 4
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
blank = pygame.image.load('people\hud_blank.png').convert_alpha()


class player(spritelings.actor):
    def __init__(self, pos):
        super().__init__(pc_pict.subsurface(0, 0, 64, 64), pos)
        self.hp = 100

        self.name = 'PC'
        self.image = pc_pict.subsurface(0, 0, 64, 64)

        #this is a image lookup dict for the directional images of the player sprite image. note that only one parent image is loaded
        #the first time this module is imported, and all the directional images are subsurfacxes of that image
        self.dirct = {(0,-1): pc_pict.subsurface(0, 0, 64, 64), (0,1): pc_pict.subsurface(128, 0, 64, 64),
                      (-1,0): pc_pict.subsurface(192, 0, 64, 64),  (1,0): pc_pict.subsurface(64, 0, 64, 64),
                      (1,1):  pc_pict.subsurface(64, 64, 64, 64), (-1, 1):  pc_pict.subsurface(0, 64, 64, 64),
                      (1,-1):  pc_pict.subsurface(192, 64, 64, 64), (-1,-1):  pc_pict.subsurface(128, 64, 64, 64)}

        self.pos = pos
        self.cast_from = self.pos
        self.facing = (0,-1)

        #hp, focus, etc will go here
        self.cooldown = 0
        self.hp = 100
        self.focus = 0
        self.max_focus = 100

        #currently unsued, but will eventually be the variable that determines which animations to use,
        #whether the player is in control, stunned, flashing, etc.
        self.state = 'normal'
        self.invincible = 0
        self.stunned = 0
        self.firing = 0

        #the spellbook is a list/set/group of all the spells the player currently has equipped
        #it is currently implemented as a dictionary that stores and indeces the constructors for
        #the missile sprites
        self.spellbook = {0:missiles.acid_bolt ,1:missiles.freeze_ray, 2:missiles.heat_ray, 3:missiles.kinetic_bolt, 4:missiles.fire_burst}
        self.page = 4
        self.spell = self.spellbook[self.page]


        #this could be anything that shares an interface with the keyboard object
        self.control_method = controller.controller(self)
        #self.control_method = keyboard_alt.keyboard(self)

        self.speed = 10

        center = self.rect.center
        self.inrect = self.rect.inflate((-16, -16))
        self.inrect.center = center


    def update(self, room):
        if self.hp <=0 :
            self.kill()

        #ticks cooldown back down, at one tick per frame.
        if self.cooldown:
            self.cooldown -= 1

        if self.invincible:
            self.invincible -= 1

        #this is the main interface method that uses the supplied control_method to accept user input and
        #control the player character
        self.control_method.update(room)

        if self.stunned > 0:
            print('I am stunned')
            self.stunned -= 1
            self.velocity = (0,0)
        if self.stunned <= 0:
            self.state = 'normal'

        #this restricts the player to the buonds of the current room.
        #basically, it checks if the player('s rect) is outside of the room('s rect) and then reverses the player's velocity
        #to keep him/her inbounds
        if room.rect.contains(self.rect.move(self.velocity)):
            self.rect.move_ip(self.velocity)
            self.inrect.move_ip(self.velocity)
            self.pos = (self.rect.x, self.rect.y)
        else:
            x = self.pos[0] - self.velocity[0]
            y = self.pos[1] - self.velocity[1]
            self.velocity = (0,0)
            self.pos = (x, y)

        self.image = self.dirct[self.facing]

    def cast(self, room):
        room.playerProjectiles.add(self.spell(self, self.facing))


    def next_spell(self):
        if self.page < len(self.spellbook) - 1:
            self.page += 1
            self.spell = self.spellbook[self.page]

    def prev_spell(self):
        if self.page > 0:
            self.page-=1
            self.spell = self.spellbook[self.page]

    def set_frame(self):
        pass

    #this feels like a really cumbersome way of applying damage and effects, but so far,
    #its all we've got.....
    def react(self, asshole):
        if self.invincible <= 0:
            self.hp = self.hp-asshole.damage
            self.rect.move_ip(asshole.velocity)
            self.stunned = 128
            self.invincible = 384
        else:
            pass
