'''
this file will house the lineage of classes derived from sprite,
allowing us to group them into different branches based on function, interaction, and behavior.
Hopefuly this will a sufficient degree of control over how the entities within the game interact.
note that I will be transitioning over into different size multipliers and image formats, so the code
below presumes the existence of spritesheets for animation purposes
'''


'''
confession: I'm not too great with python-based OOP, so I'm not sure if this level of division/inheritance is strictly necessary, 
but it does help me personally concepualize everything
'''

import pygame
import sys

#the first, most basic level of sprite: an entity
#entities have a position, an image, and a rectangle
class entity(pygame.sprite.Sprite):
    def __init__(self, pos, img):
        super().__init__()
        self.pos = pos
        self.xpos = pos[0]
        self.ypos = pos[1]
        self.image = img
        self.rect = img.get_rect().move(self.xpos, self.ypos)


#after entity, it branches into actors and reactors.
#both have 4 key methods: act, react, draw, and update.
#the key difference between the two: actors can die, reactors cannot.
#reactors are (more or less) consistent across their entire existence, and so do not need to be preserved
#actors have a great many different internal states, and need to be tracked even when not in use.

#actors move, animate, and act on things.
#this will include basically all of our 'living' things, such as:
#player character, npcs, enemies, and (potentially) wildlife
class actor(entity):
    #from entity, it will add move, anim, and react
    def __init__(self, pos, img, size):
        #calls parent constructor, note that 'size' is a tuple representing the dimensions of the object
        super().__init__(pos, img.subsurface((0,0), size))

        self.velocity = (0, 0)

    def update(self):
        pass

    def draw(self):
        pass

    #defines what the actor does to other entites upon collision
    def act(self):
        pass

    #defines how this actor responds to collision
    def react(self):
        pass


#the player character; I want to make it so that an existing Player object or an npc object can be used to create/convert a new player
class player(actor):
    def __init__(self, person):
        super().__init__(person.pos, person.img, person.size)




class enemy(actor):
    pass


#basic enemy with a simple shape (that is, one that can be reasonably approximated into a (single) recatngle
class simple(enemy):
    pass


class bitmasked(enemy):
    pass


class multi(enemy):
    pass


class segment(enemy):
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