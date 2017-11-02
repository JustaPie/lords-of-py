import pygame
import spritelings
import missiles

face = pygame.image.load("baddies\mask.png").convert_alpha()
eyes = pygame.image.load("baddies\eyes.png").convert_alpha()


class mask_of_death(spritelings.enemy):
    def __init__(self, pos):
        super().__init__(eyes, pos)
        self.name = 'Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch'
        self.eyes = eyes
        self.face = face
        self.target = None
        self.state = 'idle'
        self.sees = []
        self.mask = pygame.mask.from_surface(self.face)
        self.cooldown = 0

    #def draw(self, surf):
        #surf.blit(self.eyes)
        #surf.blit(self.image)

    def update(self, room):
        self.look(room)

    def look(self, room):
        for x in room.allSprites :
            pass
