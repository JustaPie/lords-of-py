

import pygame
import sys

pygame.init()

testMapCode = ['ffffffffffffffffffff', 'ffffffffffffffffffff','ffffffffffffffffffff','ffffffffffffffffffff','ffffffffffffffffffff','ffffffffffffffffffff','ffffffffffffffffffff','ffffffffffffffffffff','ffffffffffffffffffff','ffffffffffffffffffff']
outerBounds = ((0, len(testMapCode[0])), (0, len(testMapCode)))
print(outerBounds)

disp = pygame.display.set_mode((1560, 1000))

import room

testRoom = room.room(testMapCode)

import player

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(pygame.joystick.get_count())
jub = pygame.joystick.Joystick(0)
jub.init()
print(jub.get_name())


axes = jub.get_numaxes()
buttons = jub.get_numbuttons()
hats = jub.get_numhats()

print(axes)
print(buttons)
print(hats)

running = True
while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i in range(axes):
        axis = jub.get_axis(i)
        if axis>.5 :
            print(i)
        elif axis<-.5:
            print('-', i)

    for i in range(buttons):
        button = jub.get_button(i)
        if button :
            print(i)

    for i in range(hats):
        hat = jub.get_hat(i)
        print(hat)


    clock = pygame.time.Clock()
    msElapsed = clock.tick(600)


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