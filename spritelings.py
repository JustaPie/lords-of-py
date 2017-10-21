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

#the first, most basic level of sprite, and entity
#entities have a position, a portrait, and
class entity(pygame.sprite.Sprite):
    def __init__(self, pos, img):
        super().__init__()
        self.pos = pos
        self.xpos = pos[0]
        self.ypos = pos[1]
        self.portrait = img


#after entity, it branches into actors and interactors.

#actors move, animate, and act on things.
#this will include basically all of our 'living' things, such as:
#player character, npcs, enemies, and (potentially) wildlife
class actor(entity):
    #from entity, it will add move, anim, and react
    def __init__(self, pos, img, size):
        #calls parent constructor, note that 'size' is a tuple representing the dimensions of the object
        super().__init__(pos, img.subsurface((0,0), size))

    #defines how the actor moves
    def move(self):
        pass

    #defines how the actor is animated
    def anim(self, cycle):
        pass

    #defines what the actor does upon collision
    def act(self):
        pass


class player(actor):

class enemy(actor):

class npc(actor):

class missile(actor):


#interactors are mostly stationary, non-living things that only effect things they come into contact with
#they are passive in that things act upon them (that is, things meet their conditions) to cause stuff to happen
class interactor(entity):


class hazard(interactor):

class obstacle(interactor):

class trap(interactor):

class shiny(interactor):