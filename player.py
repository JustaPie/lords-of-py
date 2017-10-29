
import pygame
import sys

class player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.name = 'PC'

        self.image = pygame.image.load('p_arr_up.png').convert_alpha()
        self.right = pygame.transform.rotate( self.image, 90)
        self.down = pygame.transform.rotate( self.right, 90)
        self.left = pygame.transform.rotate( self.down, 90)
        self.up = pygame.transform.rotate(self.left, 90)
        self.rect = self.image.get_rect()
        print(self.rect)
        self.pos = pos
        self.xPos = pos[0]
        self.yPos = pos[1]
        self.charge = 0

    def update(self):
        if self.charge > 0:
            self.charge -= 1


    def control(self, playerProj):
        key = pygame.key.get_pressed()
        self.move(key)
        shot = self.shoot(key)
        if shot:
            self.charge = 60
            playerProj.add(shot)

    def move(self, key):
        if key[pygame.K_w]:
            self.image = self.up
            self.yPos-=5
            self.rect.move_ip(0, -5)

        if key[pygame.K_a]:
            self.image = self.left
            self.xPos-=5
            self.rect.move_ip(-5, 0)

        if key[pygame.K_s]:
            self.image = self.down
            self.yPos+=5
            self.rect.move_ip(0, 5)

        if key[pygame.K_d]:
            self.image = self.right
            self.xPos+=5
            self.rect.move_ip(5, 0)

        self.pos = (self.xPos, self.yPos)


    def shoot(self, key):
        if self.charge <= 30:
            if key[pygame.K_UP]:
                shot = icespin(self, (0,-10))
                return shot

            elif key[pygame.K_RIGHT]:
                shot = icespin(self, (10, 0))
                return shot

            elif key[pygame.K_LEFT]:
                shot = icespin(self, (-10, 0))
                return shot

            elif key[pygame.K_DOWN]:
                shot = icespin(self, (0, 10))
                return shot

            else:
                return None
        else:
            return None



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


class bullet(pygame.sprite.Sprite):
    def __init__(self, gunman, vel):
        super().__init__()

        self.image = pygame.image.load('bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.velocity = vel
        self.rect.move_ip(gunman.pos)

    def update(self):
        self.rect.move_ip(self.velocity)


class fireball(pygame.sprite.Sprite):
    def __init__(self, gunman, vel):
        super().__init__()

        self.image = pygame.image.load('fireball.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.velocity = vel
        self.rect.move_ip(gunman.pos)

    def update(self):
        self.rect.move_ip(self.velocity)


class firespin(pygame.sprite.Sprite):
    def __init__(self, gunman, vel):
        super().__init__()

        self.image = pygame.image.load('firespin.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.velocity = vel
        self.rect.move_ip(gunman.pos)

    def update(self):
        self.rect.move_ip(self.velocity)


class icespin(pygame.sprite.Sprite):
    def __init__(self, gunman, vel):
        super().__init__()

        self.image = pygame.image.load('icespin.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.velocity = vel
        self.rect.move_ip(gunman.pos)

    def update(self):
        self.rect.move_ip(self.velocity)
