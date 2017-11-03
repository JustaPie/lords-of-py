import pygame

pygame.init()

pygame.joystick.init()

jub = pygame.joystick.Joystick(0)
jub.init()


axes = jub.get_numaxes()
buttons = jub.get_numbuttons()
hats = jub.get_numhats()

#supposed to generate and return the input from a controller
class controller(object):
    def __init__(self):

    right_stick = jub.get_right_stick()
    left_stick = jub.get_left_stick()

    def get_right_stick(self):
        right_stick_x = jub.get_axes(0)
        right_stick_y = jub.get_axes(1)
        if right_stick_x > 0.15:
            x = 1
        if right_stick_x > 0.5:
            x = 2
        if right_stick_x > 0.9:
            x = 3
        if right_stick_x == 1:
            x = 4

        if right_stick_y > 0.15:
            y = 1
        if right_stick_y > 0.5:
            y = 2
        if right_stick_y > 0.9:
            y = 3
        if right_stick_y == 1:
            y = 4

        return (x, y)

    def get_left_stick(self):
        left_stick_x = jub.get_axes(3)
        left_stick_y = jub.get_axes(4)
        if left_stick_x > 0.15:
            x = 1
        if left_stick_x > 0.5:
            x = 2
        if left_stick_x > 0.9:
            x = 3
        if left_stick_x == 1:
            x = 4

        if left_stick_y > 0.15:
            y = 1
        if left_stick_y > 0.5:
            y = 2
        if left_stick_y > 0.9:
            y = 3
        if left_stick_y == 1:
            y = 4

        return (x, y)

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