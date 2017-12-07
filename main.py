import pygame, random
from pygame.locals import *

#this first bit is just useful constants
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

plyr_loc = (100, 100)
nme1_loc = (500, 500)
fps = 128
<<<<<<< HEAD
xsize = 1440
ysize = 800
screen_size = (xsize, ysize)

pygame.mixer.pre_init(44100, 16, 2, 4096)
=======
screen_size = (1500, 800)
>>>>>>> 5fd37743673fe686066d28113c92c47d6b3a32ea

pygame.init()

print('correct test')

disp = pygame.display.set_mode(screen_size)

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.music.load("audio/worms.ogg")
import player
import room
import overlays

<<<<<<< HEAD
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
    if part % 2 > 0: col = white
    else: col = grey
    particles.append( Particle(100, 800, col, round(B*part/A)) )
    particles.append(Particle(1340, 800, col,round(B*part/A)) )

test_room_code = ['ffffffffffffffff','fffffffffffffffff','fffffffffffffffff',
                  'fffffffffffffffff','fffffffffffffffff','fffffffffffffffff',
                  'fffffffffffffffff','fffffffffffffffff','fffffffffffffffff',
                  'fffffffffffffffff', 'fffffffffffffffff']
=======
size = (12, 8)
seed = 124
theme = room.theme()
dif = 1
>>>>>>> 5fd37743673fe686066d28113c92c47d6b3a32ea


test_room = room.room(disp, size, seed, theme, dif)

pc = player.player(plyr_loc)
HUD = overlays.hud(pc, disp)
hp = overlays.healthbar(pc, HUD)

test_room.addPlayer(pc)

<<<<<<< HEAD
bumper = enemies.bouncer((600, 600))
bumper.set_target(pc)
test_room.enemies.add(bumper)

#test_room.overlays.add(hp)

'''
fleye1 = enemies.fleye((500, 500))
test_room.enemies.add(fleye1)
fleye1.set_target(pc)

''''''
fleye2 = enemies.fleye((400, 400))
test_room.enemies.add(fleye2)
fleye2.set_target(pc)

fleye3 = enemies.fleye((600, 600))
test_room.enemies.add(fleye3)
fleye3.set_target(pc)
'''
intro_background = pygame.image.load("splash.png") #Load the image file
intro_background = pygame.transform.scale(intro_background, (xsize, ysize))  # Make it the same size as the screen
intro = True
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

while intro :
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




message = DynamicText(font, "???: Wake up Evaline....???: “Yes, yes, wake up!”???: “….”", (200, 200), autoreset=False)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: break
        if event.type == pygame.USEREVENT: message.update()
    else:
        disp.fill(pygame.color.Color('black'))
        message.draw(disp)
        pygame.display.flip()
        clock.tick(60)
        continue
    break
#########################################
=======
>>>>>>> 5fd37743673fe686066d28113c92c47d6b3a32ea

running = True
while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            pass

    test_room.update()
    test_room.draw_contents(disp)
    test_room.draw_boxes(disp)
    HUD.update(test_room)
    HUD.draw(disp)



    #test_room.update()
    #test_room.draw(disp)


    clock = pygame.time.Clock()
    msElapsed = clock.tick(fps)

    pygame.display.update()

    pygame.event.pump()
