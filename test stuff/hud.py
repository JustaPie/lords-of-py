import pygame
import player
import spritelings

screen_size = (1500, 1200)
blank = pygame.image.load('people\hud_blank.png').convert_alpha()
pygame.transform.scale(blank, screen_size)

class HUD(pygame.sprite.Group):
    def __init__(self, player):
        super().__init__()
        self.health_bar =