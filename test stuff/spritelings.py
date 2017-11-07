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

#here, act and react are basically get out attribute fuckup free cards.ssss
   def react(self, thing):
        pass

   def act(self, thing):
       pass


   def get_pos(self, center):
       if not center:
           return self.pos
       xC = self.rect.width/2
       yC = self.rect.height/2
       x = self.pos[0]
       y = self.pos[1]
       return (x+xC, y+yC)


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
        self.mask = pygame.mask.from_surface(self.image)


#the player character; I want to make it so that an existing Player object or an npc object can be used to create/convert a new player
class player(actor):
    pass


class enemy(actor):
    def __init__(self, img, pos):
        super().__init__(img, pos)


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