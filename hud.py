import pygame
import player
import spritelings

screen_size = (1500, 1200)
blank = pygame.image.load('people\hud_blank.png').convert_alpha()
pygame.transform.scale(blank, screen_size)

class HUD(pygame.sprite.Group):
    def __init__(self, player):
        super().__init__()

        self.hp = simple_hp_bar(player)
        self.subject = player
        self.focus = player.focus
        self.add(self.hp)

    def show(self, disp):
        pygame.rect.draw(disp, self.hp, (0, 240, 0), 8)



class simple_hp_bar(spritelings.shiny):
    def __init__(self, subject):
        super().__init__(blank, (0,0))
        self.rect = pygame.rect.Rect(0,0, subject.hp, 12)
        self.subject = subject

    def update(self):
        self.rect = pygame.rect.Rect(0, 0, self.subject.hp, 12)