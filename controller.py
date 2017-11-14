import pygame
import player

pygame.joystick.init()

jub = pygame.joystick.Joystick(0)
jub.init()
print(jub.get_name())

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

class controller(object):
    def __init__(self, player):
        self.leftstick = {'X':jub.get_axis(0), 'Y':jub.get_axis(1)}
        self.rightstick = {'X':jub.get_axis(3), 'Y':jub.get_axis(4)}
        self.triggers = {'RT':jub.get_axis(2)}
        self.buttons = {'A':jub.get_button(0), 'B':jub.get_button(1), 'X':jub.get_button(2), 'Y':jub.get_button(3),
                        'LB':jub.get_button(4), 'RB':jub.get_button(5), 'Start':jub.get_button(7), 'Select':jub.get_button(6),
                        'LStick':jub.get_button(8), 'RStick':jub.get_button(9)}
        self.subject = player

    def update(self, room):
        new_buttons = {'A':jub.get_button(0), 'B':jub.get_button(1), 'X':jub.get_button(2), 'Y':jub.get_button(3),
                    'LB':jub.get_button(4), 'RB':jub.get_button(5), 'Start':jub.get_button(7), 'Select':jub.get_button(6),
                     'LStick':jub.get_button(8), 'RStick':jub.get_button(9)}
        new_leftstick = {'X':jub.get_axis(0), 'Y':jub.get_axis(1)}
        new_rightstick = {'X': jub.get_axis(4), 'Y': jub.get_axis(3)}
        #the triggers are special, in that they are not 2 separate axies, but instead the signed difference between both triggers as a single axis
        new_triggers = {'RT': jub.get_axis(2), 'LT':jub.get_axis(2)}

        self.move(new_leftstick)
        self.subject.facing = self.look(new_rightstick, new_triggers)
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

    def look(self, stick, triggers):
        dx, dy = stick['X'], stick['Y']

        if dx and abs(dx) >= 0.3:
            print('dx= ', dx)
            dx = dx/abs(dx)
        else:
            dx = 0
        if dy and abs(dy) >= 0.3:
            dy = dy/abs(dy)
            print('dy= ', dy)
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
        if buttons['X'] and not self.subject.cooldown:
            self.subject.cast(room)


