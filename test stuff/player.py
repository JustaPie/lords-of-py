import pygame
import spritelings
import missiles
import controller
import keyboard

pc_pict = pygame.image.load('people\grn_plyr_arw.png').convert_alpha()
speed = 4
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


class player(spritelings.actor):
    def __init__(self, pos):
        super().__init__(pc_pict.subsurface(0, 0, 64, 64), pos)

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


        #the spellbook is a list/set/group of all the spells the player currently has equipped
        #it is currently implemented as a dictionary that stores and indeces the constructors for
        #the missile sprites
        self.spellbook = {1:missiles.kinetic_bolt, 2:missiles.heat_ray}
        self.spell = self.spellbook[1]
        print(self.spell)


        #this could be anything that shares an interface with the keyboard object
        self.control_method = keyboard.keyboard(self)


    def update(self, room):
        if self.hp <=0 :
            self.kill()

        #ticks cooldown back down, at one tick per frame.
        if self.cooldown > 0:
            self.cooldown -= 1

        #this is the main interface method that uses the supplied control_method to accept user input and
        #control the player character
        self.control_method.update(room)

        #this restricts the player to the buonds of the current room.
        #basically, it checks if the player('s rect) is outside of the room('s rect) and then reverses the player's velocity
        #to keep him/her inbounds
        if room.rect.contains(self.rect.move(self.velocity)):
            self.rect.move_ip(self.velocity)
        else:
            x = self.pos[0] - self.velocity[0]
            y = self.pos[1] - self.velocity[1]
            self.velocity = (0,0)
            self.pos = (x, y)

        self.image = self.dirct[self.facing]

    #this feels like a really cumbersome way of applying damage and effects, but so far,
    #its all we've got.....
    def react(self, asshole):
        if self.state == 'normal':
            self.hp = self.hp-asshole.damage

