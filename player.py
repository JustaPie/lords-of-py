
import pygame
import sys

class player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.name = 'PC'

        self.portrait = pygame.image.load('pc_cR1.png').convert_alpha()
        self.rect = self.portrait.get_rect()
        print(self.rect)
        self.xPos = pos[0]
        self.yPos = pos[1]
        self.image = self.portrait

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.yPos-=1
            self.rect = self.rect.move(0, -1)

        if key[pygame.K_a]:
            self.xPos-=1
            self.rect = self.rect.move(-1, 0)

        if key[pygame.K_s]:
            self.yPos+=1
            self.rect = self.rect.move(0, 1)

        if key[pygame.K_d]:
            self.xPos+=1
            self.rect = self.rect.move(1, 0)

        self.rect.move(self.xPos, self.yPos)

        return (self.xPos,self.yPos)


class baddy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.portrait = pygame.image.load('debug_enemy.png').convert_alpha()
        self.rect = self.portrait.get_rect()
        self.xPos = pos[0]
        self.yPos = pos[1]
        self.image = self.portrait
        self.rect = self.rect.move(self.xPos,self.yPos)

    def move(self):
        return (self.xPos, self.yPos)