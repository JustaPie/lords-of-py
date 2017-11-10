import pygame
import spritelings
import missiles

face = pygame.image.load("baddies\mask.png").convert_alpha()
eyes = pygame.image.load("baddies\eyes.png").convert_alpha()

xvf = 10
yxf = 10
accel = 2

cooling = 1
heating = 1



class mask_of_death(spritelings.enemy):
    def __init__(self, pos):
        super().__init__(face, pos)
        self.name = 'Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch'
        self.eyes = eyes
        self.face = face
        self.target = None
        self.state = 'idle'
        self.sees = []
        self.mask = pygame.mask.from_surface(self.face)
        self.cooldown = 0
        self.center = self.get_pos(1)
        self.acc = 1
        self.speed = 3
        self.target = None

        self.hp = 100

    def draw(self, surf):
        surf.blit(self.eyes, self.rect)
        surf.blit(self.image, self.rect)

    def update(self, room):
        if self.target:
            self.move_to_sprite(self.target)
        self.rect.move_ip(self.velocity)
        self.pos = (self.rect.x, self.rect.y)
        if self.hp<=0:
            self.kill()

    def set_target(self, target):
        self.target = target


    def look(self, room):
        for x in room.allSprites :
            if not x == self:
                pass


    def react(self, weapon):
        self.hp -= weapon.damage
        self.rect.move_ip(weapon.knockback)

    def act(self, victim):
        victim.hp -= 10
        victim.velocity = self.velocity

    def act(self, victim_list):
        for victim in victim_list:
            victim.hp -= 10
            victim.velocity = self.velocity
