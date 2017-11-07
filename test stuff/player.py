import pygame
import spritelings
import missiles
import controller
import keyboard

pc_pict = pygame.image.load('people\grn_plyr_arw.png').convert_alpha()
speed = 4
red = (255, 0, 0)


class player(spritelings.actor):
    def __init__(self, pos):
        super().__init__(pc_pict.subsurface(0, 0, 64, 64), pos)

        self.name = 'PC'
        self.image = pc_pict.subsurface(0, 0, 64, 64)

        #this is a image lookup dict for the directional images of the player sprite image. note that only one parent image is loaded
        #the first time this module is imported, and all the directional images are subsurfacxes of that image
        self.dirct = {'up': pc_pict.subsurface(0, 0, 64, 64),'down': pc_pict.subsurface(128, 0, 64, 64),
                      'left': pc_pict.subsurface(192, 0, 64, 64),  'right': pc_pict.subsurface(64, 0, 64, 64),
                      'dn_rt':  pc_pict.subsurface(64, 64, 64, 64), 'dn_lt':  pc_pict.subsurface(0, 64, 64, 64),
                      'up_rt':  pc_pict.subsurface(192, 64, 64, 64), 'up_lt':  pc_pict.subsurface(128, 64, 64, 64)}

        self.pos = pos

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
        self.spellbook = {1: missiles.kinetic_bolt, 'kinetic_bolt': missiles.kinetic_bolt,
                          2: missiles.fire_bolt, 'fire_bolt': missiles.fire_bolt,
                          3: missiles.ice_bolt, 'ice_bolt': missiles.ice_bolt,
                          4: missiles.acid_bolt, 'acid_bolt': missiles.acid_bolt}
        self.spell = self.spellbook[1]


        #this could be anything that shares an interface with the keyboard object
        self.control_method = keyboard.keyboard(self)




    def update(self, curRoom):
        if self.hp <=0 :
            self.kill()

        #this is a stop-gap solution until we get around to binding the fire/cast button
        #separately to the directional/facing controls
        self.control_method.cycle_spell(self)

        #ticks cooldown back down, at one tick per frame.
        if self.cooldown > 0:
            self.cooldown -= 1

        #this is the main interface method that uses the supplied control_method to accept user input and
        #control the player character
        self.control_method.update()

        #the casting of spells is done here. first it checks for cooldown
        if self.cooldown == 0:
            #cast_spell will equal NONE is the player hasn't pressed the fire key, otherwise it will be a spell
            cast_spell = self.cast()
            #this takes the spell object created above and adds it to the room's sprite group for player projectiles
            if cast_spell:
                curRoom.playerProjectiles.add(cast_spell)

        #this restricts the player to the buonds of the current room.
        #basically, it checks if the player('s rect) is outside of the room('s rect) and then reverses the player's velocity
        #to keep him/her inbounds
        if curRoom.rect.contains(self.rect.move(self.velocity)):
            self.rect.move_ip(self.velocity)
        else:
            x = self.pos[0] - self.velocity[0]
            y = self.pos[1] - self.velocity[1]
            self.pos = (x, y)

    #stop-gap helper function that calls the keyboard's cast function
    def cast(self):
        return self.control_method.cast(self)


