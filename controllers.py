import pygame
import player


def auto(player):
    pygame.joystick.init()
    if pygame.joystick.get_count():
        jub = pygame.joystick.Joystick(0)
        jub.init()
        print(jub.get_name())
        return gamepad(player)
    else:
        return keyboard(player)

'''
for the xbone controller:
AXES
left stick (x,y) = (0,1)
right stick (x,y) = (4,3)
left trigger = 2
right trigger = -2

BUTTONS
A = 0
B = 1
X = 2
Y = 3
left bumper = 4
right bumper = 5
Select = 6
Start = 7
left stick = 8
right stick = 9
'''

class gamepad(object):
    def __init__(self, player):
        self.jub = pygame.joystick.Joystick(0)
        self.jub.init()
        jub = self.jub
        print(jub.get_name())

        self.leftstick = {'X':jub.get_axis(0), 'Y':jub.get_axis(1)}
        self.rightstick = {'X':jub.get_axis(3), 'Y':jub.get_axis(4)}
        self.triggers = {'RT':jub.get_axis(2)}
        self.buttons = {'A':jub.get_button(0), 'B':jub.get_button(1), 'X':jub.get_button(2), 'Y':jub.get_button(3),
                        'LB':jub.get_button(4), 'RB':jub.get_button(5), 'Start':jub.get_button(7), 'Select':jub.get_button(6),
                        'LStick':jub.get_button(8), 'RStick':jub.get_button(9)}
        self.subject = player

    def update(self, room):
        jub = self.jub
        new_buttons = {'A':jub.get_button(0), 'B':jub.get_button(1), 'X':jub.get_button(2), 'Y':jub.get_button(3),
                    'LB':jub.get_button(4), 'RB':jub.get_button(5), 'Start':jub.get_button(7), 'Select':jub.get_button(6),
                     'LStick':jub.get_button(8), 'RStick':jub.get_button(9)}
        new_leftstick = {'X':jub.get_axis(0), 'Y':jub.get_axis(1)}
        new_rightstick = {'X': jub.get_axis(4), 'Y': jub.get_axis(3)}
        #the triggers are special, in that they are not 2 separate axies, but instead the signed difference between both triggers as a single axis
        new_triggers = {'RT': jub.get_axis(2), 'LT':jub.get_axis(2)}

        self.move(new_leftstick)
        self.subject.facing = self.look(new_rightstick)
        self.magic(new_buttons, new_triggers, room)

        self.buttons = new_buttons
        self.rightstick = new_rightstick
        self.leftstick = new_leftstick
        self.triggers = new_triggers


    def move(self, stick):
        xvel, yvel = 0, 0
        dx, dy = stick['X'], stick['Y']
        if abs(dx) > 0.05:
            xvel = self.subject.speed * dx

        if abs(dy) > 0.05:
            yvel = self.subject.speed * dy

        self.subject.velocity = (xvel, yvel)

    def look(self, stick):
        dx, dy = stick['X'], stick['Y']

        if dx and abs(dx) >= 0.5:
            dx = dx/abs(dx)
        else:
            dx = 0
        if dy and abs(dy) >= 0.5:
            dy = dy/abs(dy)
        else:
            dy = 0
        if dx or dy:
            return (dx, dy)
        else:
            return self.subject.facing

    def magic(self, buttons, triggers, room):
        if buttons['RB'] and not self.buttons['RB']:
            self.subject.next_spell()
            print(self.subject.spell)
        if buttons['LB'] and not self.buttons['LB']:
            self.subject.prev_spell()
            print(self.subject.spell)
        if buttons['X'] and not self.buttons['X']:
            self.subject.cast(room)
        self.subject.spell.charge(triggers)



class keyboard(object):
    def __init__(self, player):
        self.key = pygame.key.get_pressed()
        self.subject = player
        self.cycle_nxt = 0
        self.cycle_prev = 0
        self.cast = 0


    def update(self, room):
        self.key = pygame.key.get_pressed()
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

        fire = self.key[pygame.K_f]
        nxt = self.key[pygame.K_e]
        prv = self.key[pygame.K_q]
        squid = (fire, nxt, prv, locked)

        self.move(self.subject)
        if any(look):
            self.subject.facing = self.face(self.subject, look)

        self.magic(self.subject, room, squid)
        self.cycle_nxt = nxt
        self.cycle_prev = prv
        self.cast = fire

    def move(self, player):
        self.key = pygame.key.get_pressed()
        yVel = 0
        xVel = 0
        xdir = 0
        ydir = 0
        if self.key[pygame.K_w]:
            yVel = -player.speed
            ydir = -1
        if self.key[pygame.K_s]:
            yVel = player.speed
            ydir = 1

        if self.key[pygame.K_a]:
            xVel = -player.speed
            xdir = -1
        if self.key[pygame.K_d]:
            xVel = player.speed
            xdir = 1

        player.velocity = (xVel, yVel)
        if xdir or ydir:
            # player.facing= (xdir, ydir)
            return (xdir, ydir)
        else:
            return player.facing

    def magic(self, player, room, squid):

        if squid[0] and not self.cast:
            player.cast(room)
        if squid[1] or squid[2]:
            if squid[1] and not self.cycle_nxt:
                player.next_spell()
            elif squid[2] and not self.cycle_prev:
                player.prev_spell()
        else:
            self.firing = 0
            return None

    # this determines in which direction the player faces, and therefore which directional image to use. This should be eventually combined
    # with the cast function, since they overlap in function.
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
        if xface or yface:
            # player.facing = (xface, yface)
            return (xface, yface)
        else:
            return None


