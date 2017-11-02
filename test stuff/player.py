import pygame
import spritelings
import missiles

pc_pict = pygame.image.load('people\grn_plyr_arw.png')


class player(spritelings.actor):
    def __init__(self, pos):
        super().__init__(pc_pict, pos)

        self.name = 'PC'
        self.image = pc_pict.subsurface(0, 0, 64, 64)

        #soooo.... not sure if this runs only once, during the first use of the socnstructor, or not
        self.dirct = {'up': pc_pict.subsurface(0, 0, 64, 64), 'right': pc_pict.subsurface(64, 0, 64, 64), 'down': pc_pict.subsurface(128, 0, 64, 64), 'left': pc_pict.subsurface(192, 0, 64, 64), 'dn_rt':  pc_pict.subsurface(64, 64, 64, 64), 'dn_lt':  pc_pict.subsurface(0, 64, 64, 64), 'up_rt':  pc_pict.subsurface(192, 64, 64, 64), 'up_lt':  pc_pict.subsurface(128, 64, 64, 64)}

        self.pos = pos

        self.cooldown = 0
        self.hp = 100
        self.focus = 0
        self.max_focus = 100

        self.spellbook = {1: missiles.kinetic_bolt, 'kinetic_bolt': missiles.kinetic_bolt}
        self.spell = self.spellbook[1]


    def update(self, curRoom):
        if self.cooldown > 0:
            self.cooldown -= 1

        key = pygame.key.get_pressed()
        self.move(key)
        self.rect.move_ip(self.velocity)
        self.face(key)

        if self.cooldown == 0:
            cast_spell = self.cast(key)
            if cast_spell:
                self.cooldown = cast_spell.cooldown
                curRoom.playerProjectiles.add(cast_spell)



    def cast(self, key):
        xFace = 0
        yFace = 0
        if key[pygame.K_UP]:
            yFace = -1
        elif key[pygame.K_DOWN]:
            yFace = 1

        if key[pygame.K_RIGHT]:
            xFace = 1
        elif key[pygame.K_LEFT]:
            xFace = -1

        if xFace or yFace :
            print('spell should cast')

            return self.spell(self, (xFace, yFace))
        else:
            return None


    def move(self, key):
        yVel = 0
        xVel = 0
        if key[pygame.K_w]:
            self.image = self.dirct['up']
            yVel = -6
        if key[pygame.K_s]:
            self.image = self.dirct['down']
            yVel = 6

        if key[pygame.K_a]:
            xVel = -6
        if key[pygame.K_d]:
            xVel = 6


        self.velocity = (xVel, yVel)
        xPos = self.pos[0]
        yPos = self.pos[1]
        self.pos = (xPos+xVel, yPos+yVel)

    def face(self, key):
        x = self.velocity[0]
        y = self.velocity[1]

        if x > 0:
            self.image = self.dirct['right']
            if y > 0:
                self.image = self.dirct['dn_rt']
            elif y < 0:
                self.image = self.dirct['up_rt']
        elif x < 0:
            self.image = self.dirct['left']
            if y > 0:
                self.image = self.dirct['dn_lt']
            elif y < 0:
                self.image = self.dirct['up_lt']

        if key[pygame.K_UP]:
            self.image = self.dirct['up']
            if key[pygame.K_RIGHT]:
                self.image = self.dirct['up_rt']
            elif key[pygame.K_LEFT]:
                self.image = self.dirct['up_lt']

        elif key[pygame.K_DOWN]:
            self.image = self.dirct['down']
            if key[pygame.K_RIGHT]:
                self.image = self.dirct['dn_rt']
            elif key[pygame.K_LEFT]:
                self.image = self.dirct['dn_lt']

        elif key[pygame.K_LEFT]:
            self.image = self.dirct['left']

        elif key[pygame.K_RIGHT]:
            self.image = self.dirct['right']
