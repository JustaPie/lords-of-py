
import pygame
import sys

class player (pygame.sprite.Sprite):
    def __init__(self):
        self.name = 'PC'

        self.portrait = pygame.image.load("pc_cR.png').convert_alpha()
        self.box = pygame.get_rect(self.pict)


    def walk(self):

    def slide(self):

