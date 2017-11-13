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
        #new_triggers =

        self.move(new_leftstick)
        self.subject.facing = self.look(new_rightstick)


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

