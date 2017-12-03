import pygame
import spritelings

class wall(spritelings.block):
    pass

class fence(wall):
    pass

class door(spritelings.block):
    def __init__(self, dest_room_seed, dest_room = None, dest_loc = (50, 50), *args):
        pass