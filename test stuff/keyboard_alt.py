

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
        self.cycle_nxt = 0
        self.cycle_prev = 0
        self.timer = 0
        self.firing = 0

    def update(self, room):
        self.key = pygame.key.get_pressed()
        self.timer+=1
        mov_up = self.key[pygame.K_w]
        mov_dn = self.key[pygame.K_s]
        mov_lt = self.key[pygame.K_a]
        mov_rt = self.key[pygame.K_d]
        move = (mov_up, mov_dn, mov_lt, mov_rt)

        locked = self.key[pygame.K_LSHIFT]

        lk_up = self.key[pygame.K_UP]
        lk_dn = self.key[pygame.K_DOWN]
        lk_lt = self.key[pygame.K_LEFT]
        lk_rt = self.key[pygame.K_RIGHT]
        look = (lk_up, lk_dn, lk_lt, lk_rt)

        fire = self.key[pygame.K_SPACE]
        nxt = self.key[pygame.K_e]
        prv = self.key[pygame.K_q]
        squid = (fire, nxt, prv, locked)

        self.move(self.subject)
        #look_face = self.face(self.subject, look)
        if any in look:
            self.subject.facing = self.face(self.subject, look)

        self.magic(self.subject, room, squid)
        self.cycle_nxt = nxt
        self.cycle_prev = prv

        if self.timer%32 ==0:
            print("squid= ", squid)
            print('look = ', look)
            print('move= ', move)

    def move(self, player):
        self.key = pygame.key.get_pressed()
        yVel = 0
        xVel = 0
        xdir = 0
        ydir = 0
        if self.key[pygame.K_w]:
            yVel = -speed
            ydir = -1
        if self.key[pygame.K_s]:
            yVel = speed
            ydir = 1

        if self.key[pygame.K_a]:
            xVel = -speed
            xdir = -1
        if self.key[pygame.K_d]:
            xVel = speed
            xdir = 1

        player.velocity = (xVel, yVel)
        xPos = player.pos[0]
        yPos = player.pos[1]
        player.pos = (xPos + xVel, yPos + yVel)
        if xdir or ydir:
            #player.facing= (xdir, ydir)
            return (xdir, ydir)
        else:
            return player.facing

    def not_move(self, player, move):
        yVel = 0
        xVel = 0
        xdir = 0
        ydir = 0
        if move[0]:
            yVel = -speed
            ydir = -1
        if move[1]:
            yVel = speed
            ydir = 1

        if move[2]:
            xVel = -speed
            xdir = -1
        if move[3]:
            xVel = speed
            xdir = 1

        player.velocity = (xVel, yVel)
        xPos = player.pos[0]
        yPos = player.pos[1]
        player.pos = (xPos + xVel, yPos + yVel)
        if xdir or ydir:
            # player.facing= (xdir, ydir)
            return (xdir, ydir)
        else:
            return player.facing




#'''
#here, what I want to do is bind the cast command to spacebar, or some other button, such that
#the arrow keys only control which direction the player is facing. There's prbly some fancy way to handle this with decorators
#and/or encapsulators,
#'''
    def magic(self, player, room, squid):

        if squid[0] and not self.firing and player.cooldown == 0      :
            player.cast(room)
            #player.state = 'firing'
            self.firing = 1
            return None
        if squid[1] or squid[2]:
            if squid[1] and not self.cycle_nxt:
                player.next_spell()
            elif squid[2] and not self.cycle_prev:
                player.prev_spell()
        else:
            self.firing = 0
            return None

    #this determines in which direction the player faces, and therefore which directional image to use. This should be eventually combined
    #with the cast function, since they overlap in function.
    def not_face(self, player, look):
        self.key = pygame.key.get_pressed()
        xface = 0
        yface = 0
        if look[0]:
            yface = -1
        if look[1]:
            yface = 1

        if look[2]:
            xface = -1
        if look[3]:
            xface = 1
        if self.timer % 32 ==0:
            print('xface: ', xface, 'yface: ', yface)

        if xface or yface:
            #player.facing = (xface, yface)
            return (xface, yface)
        else:
            return None

    def face(self, player, look):
        self.key = pygame.key.get_pressed()
        xface = 0
        yface = 0
        if self.key[pygame.K_UP]:
            yface = -1
        if self.key[pygame.K_DOWN]:
            yface = 1

        if self.key[pygame.K_LEFT]:
            xface = -1
        if self.key[pygame.K_RIGHT]:
            xface = 1
        if self.timer % 32 ==0:
            print('xface: ', xface, 'yface: ', yface)

        if xface or yface:
            #player.facing = (xface, yface)
            return (xface, yface)
        else:
            return None