import pygame
from pygame.locals import *

#this first bit is just useful constants
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

fps = 128
xsize = 1500
ysize = 800
screen_size = (xsize, ysize)

game_over = pygame.image.load("bits&bobs/you are dead.png") #Load the image file
game_over = pygame.transform.scale(game_over, (xsize, ysize))  # Make it the same size as the scree


pygame.init()

print('correct test')

disp = pygame.display.set_mode(screen_size)

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.music.load("audio/worms.ogg")


bkgd = pygame.image.load("Fog.png").convert_alpha()
scroll = 0

import player
import room
import missiles
import enemies
import overlays
import random
size = (12, 8)
seed = None #enemies.fleye((500, 500))
theme = room.theme()
dif = 1

class Particle():
    def __init__(self, startx, starty, col, pause):
        self.x = startx
        self.y = starty
        self.col = col
        self.sx = startx
        self.sy = starty
        self.pause = pause

    def move(self):
        if self.pause==0:
            if self.y < 0:
                self.x=self.sx
                self.y=self.sy

            else:
                self.y-=1

            self.x+=random.randint(-2, 2)

        else:
            self.pause-=1
white = (255, 255, 255)
black = (0,0,0)
grey = (128,128,128)
clock=pygame.time.Clock()

particles = []
A=300#num particles
B=800#y value start
for part in range(1, 300):
    if part % 2 > 0: col = red
    else: col = grey
    particles.append( Particle(100, 800, col, round(B*part/A)) )
    particles.append(Particle(1340, 800, col,round(B*part/A)) )




test_room = room.room(disp, size, seed, theme, dif)

pc = player.player((0,0))
HUD = overlays.hud(pc, disp)
hp = overlays.healthbar(pc, HUD)

test_room.addPlayer(pc)


intro_background = pygame.image.load("splash.png") #Load the image file
intro_background = pygame.transform.scale(intro_background, (xsize, ysize))  # Make it the same size as the screen
intro = True
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

while intro:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            intro = False
    disp.blit(intro_background, (0, 0))

    for p in particles:
        p.move()
        pygame.draw.circle(disp, p.col, (p.x, p.y), 2)

    pygame.display.flip()
    clock.tick(50)
#########################################
font = pygame.font.Font(None, 25)
pygame.time.set_timer(pygame.USEREVENT, 200)
def text_generator(text):
    tmp = ''
    for letter in text:
        tmp += letter
        # don't pause for spaces
        if letter != ' ':
            yield tmp

class DynamicText(object):
    def __init__(self, font, text, pos, autoreset=False):
        self.done = False
        self.font = font
        self.text = text
        self._gen = text_generator(self.text)
        self.pos = pos
        self.autoreset = autoreset
        self.update()

    def reset(self):
        self._gen = text_generator(self.text)
        self.done = False
        self.update()

    def update(self):
        if not self.done:
            try:
                self.rendered = self.font.render(next(self._gen), True, (0, 128, 0))
            except StopIteration:
                self.done = True
                if self.autoreset: self.reset()

    def draw(self, disp):
        disp.blit(self.rendered, self.pos)


#########################################################################################

#very long winded way to display dialogue....there has to be a better way.
message1 = DynamicText(font, "???: “Wake up Evaline.”", (200, 200), autoreset=False)
message2 = DynamicText(font, "???: “Yes, yes, wake up!”", (200, 225), autoreset=False)
message3 = DynamicText(font, "???: “.......”", (200, 250), autoreset=False)

message4 = DynamicText(font, "???: “Do you remember us from your dreams, Evaline?”", (200, 200), autoreset=False)
message5 = DynamicText(font, "???: “You didn't forget about me now did you? That would hurt my feelings!”", (200, 225), autoreset=False)
message6 = DynamicText(font, "???: “.......”", (200, 250), autoreset=False)

message7 = DynamicText(font, "???: “You do remember, don’t you? You can’t recall why, yet you feel something.”", (200, 200), autoreset=False)
message8 = DynamicText(font, "???: “Enough with the silence, say something already!”", (200, 225), autoreset=False)
message9 = DynamicText(font, "???: “.......”", (200, 250), autoreset=False)

message10 = DynamicText(font, "???: “I want to help you. You’ve been in the void for a while now. It’s time someone completed you.”", (200, 200), autoreset=False)
message11 = DynamicText(font, "???: “You’re just a tool, let’s be honest. But potentially a very useful tool. The more you can do, the more useful you will be to me.”", (200, 225), autoreset=False)
message12 = DynamicText(font, "???: “.......”", (200, 250), autoreset=False)

message13 = DynamicText(font, "???: “Are you ready to take the next step? To see what you can become?”", (200, 200), autoreset=False)
message14 = DynamicText(font, "???: “So, what are you? Will you continue to be a lifeless doll? Or do you desire power and purpose? I can give you what you seek…. for a price.”", (200, 225), autoreset=False)
message15 = DynamicText(font, "???: “.......”", (200, 250), autoreset=False)

message16 = DynamicText(font, "[I'm ready.]", (200, 250), autoreset=False)


counter = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            break
        if event.type == pygame.USEREVENT:
            if counter == 1:
                message1.update()
            elif counter == 2:
                message2.update()
            elif counter == 3:
                message3.update()
            elif counter == 4:
                message4.update()
            elif counter == 5:
                message5.update()
            elif counter == 6:
                message6.update()
            elif counter == 7:
                message7.update()
            elif counter == 8:
                message8.update()
            elif counter == 9:
                message9.update()
            elif counter == 10:
                message10.update()
            elif counter == 11:
                message11.update()
            elif counter == 12:
                message12.update()
            elif counter == 13:
                message13.update()
            elif counter == 14:
                message14.update()
            elif counter == 15:
                message15.update()
            elif counter == 16:
                message16.update()

    else:
        disp.fill(pygame.color.Color('black'))
        if counter == 1:
            message1.draw(disp)
        if counter == 2:
            message1.draw(disp)
            message2.draw(disp)
        if counter == 3:
            message1.draw(disp)
            message2.draw(disp)
            message3.draw(disp)
        if counter == 4:
            message4.draw(disp)
        if counter == 5:
            message4.draw(disp)
            message5.draw(disp)
        if counter == 6:
            message4.draw(disp)
            message5.draw(disp)
            message6.draw(disp)
        if counter == 7:
            message7.draw(disp)
        if counter == 8:
            message7.draw(disp)
            message8.draw(disp)
        if counter == 9:
            message7.draw(disp)
            message8.draw(disp)
            message9.draw(disp)
        if counter == 10:
            message10.draw(disp)
        if counter == 11:
            message10.draw(disp)
            message11.draw(disp)
        if counter == 12:
            message10.draw(disp)
            message11.draw(disp)
            message12.draw(disp)
        if counter == 13:
            message13.draw(disp)
        if counter == 14:
            message13.draw(disp)
            message14.draw(disp)
        if counter == 15:
            message13.draw(disp)
            message14.draw(disp)
            message15.draw(disp)
        if counter == 16:
            message16.draw(disp)

        if message1.done:
            counter = 2
        if message2.done:
            counter = 3
        if message3.done:
            counter = 4
        if message4.done:
            counter = 5
        if message5.done:
            counter = 6
        if message6.done:
            counter = 7
        if message7.done:
            counter = 8
        if message8.done:
            counter = 9
        if message9.done:
            counter = 10
        if message10.done:
            counter = 11
        if message11.done:
            counter = 12
        if message12.done:
            counter = 13
        if message13.done:
            counter = 14
        if message14.done:
            counter = 15
        if message15.done:
            counter = 16
        pygame.display.flip()
        clock.tick(60)
        continue
    break


running = True
while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()           
        elif event.type == pygame.KEYDOWN:
            pass
        elif event.type == player.heros_death:
            disp.blit(game_over, (0, 0))
            running = False

    test_room.update()
    test_room.draw_contents(disp)
    test_room.draw_boxes(disp)
    HUD.update(test_room)
    HUD.draw(disp)

    clock = pygame.time.Clock()
    msElapsed = clock.tick(fps)


    rel = scroll % bkgd.get_rect().width
    disp.blit(bkgd, (rel - bkgd.get_rect().width, 0))
    
    if rel < 1600:
        disp.blit(bkgd, (rel,0))

    scroll += 2


    pygame.display.update()

    pygame.event.pump()

    if len(test_room.enemies)==0:
        player.hp = 600
        dif += 1
        test_room.next_level(pc, dif)

####################################################    GAME OVER         #######################


pygame.mixer.music.load("audio/game_over.wav")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play()

while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    else:
        disp.blit(game_over, (0, 0))
        pygame.display.update()



