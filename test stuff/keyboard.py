

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

    def update(self, room):
        self.key = pygame.key.get_pressed()
        mov_up = self.key[pygame.K_w]
        mov_dn = self.key[pygame.K_s]
        mov_lt = self.key[pygame.K_a]
        mov_rt = self.key[pygame.K_d]
        move = (mov_up, mov_dn, mov_lt, mov_rt)

        locked = self.key[pygame.KMOD_SHIFT]

        lk_up = self.key[pygame.K_UP]
        lk_dn = self.key[pygame.K_DOWN]
        lk_lt = self.key[pygame.K_LEFT]
        lk_rt = self.key[pygame.K_RIGHT]
        look = (lk_up, lk_dn, lk_lt, lk_rt)

        facing = self.face(self.subject, look)
        if not facing:
            facing = self.move(self.subject, move)
        else:
            self.move(self.subject, move)

        if not locked and facing:
            player.facing = facing

        fire = self.key[pygame.K_SPACE]
        nxt = self.key[pygame.K_e]
        prv = self.key[pygame.K_q]
        squid = (fire, nxt, prv)
        self.magic(player, room, squid)



    def move(self, player, move):
        yVel = 0
        xVel = 0
        xdir = 0
        ydir = 0
        if move[0]:
            yVel = -speed
            ydir -= 1
        if move[1]:
            yVel = speed
            ydir += 1

        if move[2]:
            xVel = -speed
            xdir -= 1
        if move[3]:
            xVel = speed
            xdir += 1

        player.velocity = (xVel, yVel)
        xPos = player.pos[0]
        yPos = player.pos[1]
        player.pos = (xPos + xVel, yPos + yVel)
        return (xdir, ydir)




#'''
#here, what I want to do is bind the cast command to spacebar, or some other button, such that
#the arrow keys only control which direction the player is facing. There's prbly some fancy way to handle this with decorators
#and/or encapsulators,
#'''
    def magic(self, player, room, squid):
        if squid[0]:
            pass
        elif squid[1] or squid[2]:
            pass

        else:
            return None

    def cast(self, player):

    def cycle_spell(self, player):
        for event in pygame.event.get():
            if



    #this determines in which direction the player faces, and therefore which directional image to use. This should be eventually combined
    #with the cast function, since they overlap in function.
    def face(self, player, look):
        xface = 0
        yface = 0
        if look[0]:
            yface = -1
        elif look[1]:
            yface = 1

        if look[2]:
            xface = -1
        elif look[3]:
            xface = 1

        if xface or yface:
            return player.facing
        else:
            return None