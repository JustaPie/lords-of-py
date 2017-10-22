
import pygame
import sys

class player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.name = 'PC'

        self.left =  pygame.image.load('p_arr_lt.png').convert_alpha()
        self.right = pygame.image.load('p_arr_rt.png').convert_alpha()
        self.up = pygame.image.load('p_arr_up.png').convert_alpha()
        self.down = pygame.image.load('p_arr_dn.png').convert_alpha()
        self.image = self.up
        self.rect = self.image.get_rect()
        print(self.rect)
        self.xPos = pos[0]
        self.yPos = pos[1]

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.image = self.up
            self.yPos-=1
            self.rect = self.rect.move(0, -1)

        if key[pygame.K_a]:
            self.image = self.left
            self.xPos-=1
            self.rect = self.rect.move(-1, 0)

        if key[pygame.K_s]:
            self.image = self.down
            self.yPos+=1
            self.rect = self.rect.move(0, 1)

        if key[pygame.K_d]:
            self.image = self.right
            self.xPos+=1
            self.rect = self.rect.move(1, 0)

        print(self.rect)
        return (self.xPos,self.yPos)


class baddy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load('debug_enemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.xPos = pos[0]
        self.yPos = pos[1]
        self.image = self.image
        self.rect = self.rect.move(self.xPos,self.yPos)

    def move(self):
        return (self.xPos, self.yPos)