import pygame
import spritelings


disin_orbs_name = './images/missiles/disin_orbs.png'
disin_orbs = pygame.image.load(disin_orbs_name).convert_alpha()
disin_orb_s = pygame.Surface.subsurface((0, 0, 30, 30))
disin_orb_m = pygame.Surface.subsurface((30, 0, 60, 60))