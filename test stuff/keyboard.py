

'''
this class/module essentially defines a keyboard as an object with methods that retreive keyboard input
and then use that to affect a sprite, currently this is only the player
this was originally built in to the player cass, but I separated the two so that the control
interface could be easily changed, say into a controller/gamepad
'''
import pygame
import player

speed = 4

pygame.init()


class keyboard(object):
    def __init__(self, player):
        self.key = pygame.key.get_pressed()
        self.subject = player
        self.current_spell = 1

    def update(self):
        self.key = pygame.key.get_pressed()
        self.move(self.subject)
        self.face(self.subject)


    def move(self, player):
        yVel = 0
        xVel = 0
        if self.key[pygame.K_w]:
            player.image = player.dirct['up']
            yVel = -speed
        if self.key[pygame.K_s]:
            player.image = player.dirct['down']
            yVel = speed

        if self.key[pygame.K_a]:
            xVel = -speed
        if self.key[pygame.K_d]:
            xVel = speed

        player.velocity = (xVel, yVel)
        xPos = player.pos[0]
        yPos = player.pos[1]
        player.pos = (xPos + xVel, yPos + yVel)




#'''
#here, what I want to do is bind the cast command to spacebar, or some other button, such that
#the arrow keys only control which direction the player is facing. There's prbly some fancy way to handle this with decorators
#and/or encapsulators,
#'''

    def cast(self, player):
        xFace = 0
        yFace = 0

        if self.key[pygame.K_UP]:
            yFace = -1
        elif self.key[pygame.K_DOWN]:
            yFace = 1

        if self.key[pygame.K_RIGHT]:
            xFace = 1
        elif self.key[pygame.K_LEFT]:
            xFace = -1

        if xFace or yFace:
           return player.spell(player, (xFace, yFace))
        else:
            return None

    def cycle_spell(self, player):
        if player.cooldown ==  0 :
            if self.key[pygame.K_q]:
                print('next spell')
                self.current_spell = 1
            elif self.key[pygame.K_e]:
                print('prev spell')
                self.current_spell = 2
            player.spell = player.spellbook[self.current_spell]
            #player.cooldown = 16


    #this determines in which direction the player faces, and therefore which directional image to use. This should be eventually combined
    #with the cast function, since they overlap in function.
    def face(self, player):
        x = player.velocity[0]
        y = player.velocity[1]

        xFace = 0
        yFace = 0

        if x > 0:
            xFace = 1
            player.image = player.dirct['right']
            i = player.pos[0]+player.rect.width
            j = player.pos[1] + 32
            player.cast_from = (i, j)
            if y > 0:
                yFace = 1
                player.image = player.dirct['dn_rt']
            elif y < 0:
                yFace = -1
                player.image = player.dirct['up_rt']
        elif x < 0:
            xFace = -1
            player.image = player.dirct['left']
            if y > 0:
                yFace = 1
                player.image = player.dirct['dn_lt']
            elif y < 0:
                yFace = -1
                player.image = player.dirct['up_lt']

        if self.key[pygame.K_UP]:
            player.image = player.dirct['up']
            if self.key[pygame.K_RIGHT]:
                player.image = player.dirct['up_rt']
            elif self.key[pygame.K_LEFT]:
                player.image = player.dirct['up_lt']

        elif self.key[pygame.K_DOWN]:
            player.image = player.dirct['down']
            if self.key[pygame.K_RIGHT]:
                player.image = player.dirct['dn_rt']
            elif self.key[pygame.K_LEFT]:
                player.image = player.dirct['dn_lt']

        elif self.key[pygame.K_LEFT]:
            player.image = player.dirct['left']

        elif self.key[pygame.K_RIGHT]:
            player.image = player.dirct['right']