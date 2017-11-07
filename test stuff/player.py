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

        #soooo.... not sure if this runs only once, during the first use of the socnstructor, or not
        self.dirct = {'up': pc_pict.subsurface(0, 0, 64, 64),'down': pc_pict.subsurface(128, 0, 64, 64),
                      'left': pc_pict.subsurface(192, 0, 64, 64),  'right': pc_pict.subsurface(64, 0, 64, 64),
                      'dn_rt':  pc_pict.subsurface(64, 64, 64, 64), 'dn_lt':  pc_pict.subsurface(0, 64, 64, 64),
                      'up_rt':  pc_pict.subsurface(192, 64, 64, 64), 'up_lt':  pc_pict.subsurface(128, 64, 64, 64)}

        self.pos = pos

        self.cooldown = 0
        self.hp = 100
        self.focus = 0
        self.max_focus = 100

        #the spellbook is a list/set/group of all the spells the player currently has equipped
        #it is currently implemented as a dictionary that stores and indeces the constructors for
        #the missile sprites
        self.spellbook = {1: missiles.kinetic_bolt, 'kinetic_bolt': missiles.kinetic_bolt,
                          2: missiles.fire_bolt, 'fire_bolt': missiles.fire_bolt,
                          3: missiles.ice_bolt, 'ice_bolt': missiles.ice_bolt,
                          4: missiles.acid_bolt, 'acid_bolt': missiles.acid_bolt}
        self.spell = self.spellbook[1]


        self.control_method = keyboard.keyboard(self)




    def update(self, curRoom):
        if self.hp <=0 :
            self.kill()

        self.control_method.cycle_spell(self)

        if self.cooldown > 0:
            self.cooldown -= 1
        self.control_method.update()


        if self.cooldown == 0:
            cast_spell = self.cast()
            if cast_spell:
                curRoom.playerProjectiles.add(cast_spell)

        if curRoom.rect.contains(self.rect.move(self.velocity)):
            self.rect.move_ip(self.velocity)
        else:
            x = self.pos[0] - self.velocity[0]
            y = self.pos[1] - self.velocity[1]
            self.pos = (x, y)

    def cast(self):
        return self.control_method.cast(self)


