import pygame

pygame.joystick.init()

jub = pygame.joystick.Joystick(0)
jub.init()
print(jub.get_name())

'''
for the xbone controller:
AXES
righstick (x,y) = (0,1)
leftstick (x,y) = (4,3)
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
    def __init__(self):
        self.rightstick = (jub.get_axis(0), jub.get_axis(1))
        self.leftstick = (jub.get_axis(4), jub.get_axis(3))
        self.triggers = (jub.get_axis(2))


    def get_R_stick(self):
        pass

    def get_L_stick(self):
        self.leftstick = self.leftstick = (jub.get_axis(4), jub.get_axis(3))

    def control_player(self, player):
        player.velocity = self.get_L_stick




blah = controller()