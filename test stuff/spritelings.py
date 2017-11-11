'''
this file will house the lineage of classes derived from sprite,
allowing us to group them into different branches based on function, interaction, and behavior.
Hopefuly this will a sufficient degree of control over how the entities within the game interact.
note that I will be transitioning over into different size multipliers and image formats, so the code
below presumes the existence of spritesheets for animation purposes
'''



'''
this details the basic structure of inheritance for every type of sprite we'll be using, and holds all the generic methods that we intend to 
pass downwards via inheritance to more specialized classes. basically, if you plan to use a particular method many times for many different sprites,
find the common ancestor of all the sprites that you want to have access to the method, and define it for the ancestor.
ex: entity is the common ancestor of all our sprite(s/classes), so to give all sprites access to a method, simply define it for the entity class
'''

import pygame
import sys
import math
from fractions import Fraction

#basically a simple way to store a pocket of data that will need to be copied repeatedly
class anim_frame(object):
    def __init__(self, img):
        self.image = img
        self.rect = img.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


#the first, most basic level of sprite: an entity
#entities have an image and a rectangle
class entity(pygame.sprite.Sprite):
   def __init__(self, img, pos):
       super().__init__()

       self.image = img
       self.rect = img.get_rect()
       self.pos = pos
       self.rect.move_ip(pos)
       self.velocity = (0, 0)
       self.mask = pygame.mask.from_surface(self.image)

#there's prbly a way to set this up so that we can use pre-loaded assets to quickly construct things
   def gen_anim(self, asset, pos):
       self.img = asset.img
       self.rect = asset.rect
       self.mask = asset.mask
       self.rect.move_ip(pos)
       self.velocity = (0,0)



#here, act and react are basically get out attribute fuckup free cards.ssss
   def react(self, thing):
        pass

   def act(self, thing):
       pass


   def get_pos(self, center = 0):
       if not center:
           return self.pos
       xC = self.rect.width/2
       yC = self.rect.height/2
       x = self.pos[0]
       y = self.pos[1]
       return (x+xC, y+yC)

   def set_image(self, new_image):
       self.image = new_image
       self.rect = self.image.get_rect()
       self.mask = pygame.mask.from_surface(self.image)
       self.rect.move_ip(self.pos)


#after entity, it branches into actors and reactors.
#both have 4 key methods: act, react, draw, and update.
#the key difference between the two: actors can die, reactors cannot.
#reactors are (more or less) consistent across their entire existence, and so do not need to be preserved
#actors have a great many different internal states, and need to be tracked even when not in use.

#actors move, animate, and act on things.
#this will include basically all of our 'living' things, such as:
#player character, npcs, enemies, and (potentially) wildlife
class actor(entity):
    def __init__(self, img, pos):
        super().__init__(img, pos)



#the player character; I want to make it so that an existing Player object or an npc object can be used to create/convert a new player
class player(actor):
    pass


class enemy(actor):
    '''def __init__(self, img, pos):
        super().__init__(img, pos)
        self.speed = 0
        self.acc = 0
        self.damage = 0

    #handler method for sequencing move orders, calculating movement vectors,
    #picking and checking locations,
    def movement(self, pattern):
        pass

    #the following vector methods have to do with adjusting
    #position, velocity, and acceleration
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
'''

#simple test enemy
class fleye(enemy):
    pass

class npc(actor):
    pass


#launched projectile. has many subtypes and attributes
#element: fire, ice, kinetic, disruptive, electric, sonic
#delivery/shape: beam, bolt, burst, blast, bubble, barrier, blade
#trigger: charge, pulse, continuous
#modifier: ray, wave, disc, stream,
class missile(actor):
    pass


#reactors are mostly stationary, non-living things that only effect things they come into contact with
#they are passive in that things act upon them (that is, things meet their conditions) to cause stuff to happen
class reactor(entity):
    pass


#an area of space that applies a constant, passive effect to actors that traverse/collide with it
#spikes, slow traps, but also buff pads. really anything that continues to react as long as you touch it
class hazard(reactor):
    pass


#square or rectangular block (occlusion perimeter) of non-repeating images assembled in a particular order
#this is how we will make irregularly shaped rooms
class block(reactor):
    pass


#a linear barrier composed of a repeating tile pattern
#actual fences, thin walls,
class fence(reactor):
    pass


#a stationary object with a transparent radius that does something upon collision/action w/(i) said radius
#levers, doors, buttons, certain traps
class trigger(reactor):
    pass


#a stationary, animated object
#includes flickering torches, running water, sparkling treasure
class shiny(reactor):
    pass