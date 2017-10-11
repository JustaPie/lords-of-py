import pygame
import sys

class room (pygame.Surface):
    def __init__(self):
        #key-value pairs that link each tile to an image.
        tileSet = dict([('tw', )])

        #the actual layout of each room is encoded as a list of strings, where each char represents a tile
        # these will be looked up in the tileset
        mapCode = ['wwwwwwwwww', 'wfffff<hazard_spikes, f>ffffw', 'wfffffffffw', 'wfffffffffw', 'wwwwwwwwww']

        outerBounds = ((100,800), (100,800))
        innerBounds = ((x,y), )
        hazards = ((x,y), hazardID)

        soriteList = [all sprites in the room]