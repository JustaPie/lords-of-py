
import pygame, random
from pygame.locals import *

#this first bit is just useful constants
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)


plyr_loc = (100, 100)
nme1_loc = (500, 500)
fps = 128
xsize = 1440
ysize = 800
screen_size = (xsize, ysize)

game_over = pygame.image.load("bits&bobs/you are dead.png") #Load the image file
game_over = pygame.transform.scale(game_over, (xsize, ysize))  # Make it the same size as the screen

pygame.mixer.pre_init(44100, 16, 2, 4096)

pygame.init()

print('correct test')

disp = pygame.display.set_mode(screen_size)



pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.music.load("audio/worms.ogg")
import player
import room
import missiles
import enemies
import overlays

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


test_room = room.room(test_room_code)

pc = player.player(plyr_loc)
HUD = overlays.hud(pc, disp)
hp = overlays.healthbar(pc, HUD)

test_room.addPlayer(pc)

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



#very long winded way to display dialogue....there has to be a better way.
message1 = DynamicText(font, "???: Wake up Evaline....", (200, 200), autoreset=False)
message2 = DynamicText(font, "???: Yes, yes, wake up!", (200, 225), autoreset=False)
message3 = DynamicText(font, "???: .......", (200, 250), autoreset=False)

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
        if message1.done:
            counter = 2
        if message2.done:
            counter = 3
        pygame.display.flip()
        clock.tick(60)
        continue
    break
#########################################
bkgd = pygame.image.load("Fog.png").convert_alpha()#for fog
scroll = 0 #for fog

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


    disp.blit(test_room.fSurf, (0,0))

    test_room.player.update(test_room)
    test_room.playerProjectiles.update(test_room)

    test_room.enemies.update(test_room)
    test_room.enemyProjectiles.update(test_room)

    test_room.allSprites.draw(disp)
    test_room.allProjectiles.draw(disp)

    test_room.inactivePlayerProjectiles.update(test_room)
    test_room.inactivePlayerProjectiles.draw(disp)

    test_room.nme_overlays.draw(disp)

    HUD.update(test_room)
    HUD.draw(disp)

    #player_hud.update()
    #player_hud.show(disp)

    for x in test_room.player:
        pygame.draw.rect(disp, green, x.rect, 4)
    for x in test_room.player:
        pygame.draw.rect(disp, red, x.hitbox, 4)

    for y in test_room.enemies:
        pygame.draw.rect(disp, blue, y.rect, 8)
    for y in test_room.enemies:
        pygame.draw.rect(disp, red, y.hitbox, 4)
        for z in y.hitboxes:
            pygame.draw.rect(disp, green, z, 5)

    for z in test_room.allProjectiles:
        pygame.draw.rect(disp, red, z.rect, 7)
    for z in test_room.allProjectiles:
        pygame.draw.rect(disp, green, z.hitbox, 4)


    test_room.update()


    clock = pygame.time.Clock()
    msElapsed = clock.tick(fps)

    #####fog
    rel = scroll % bkgd.get_rect().width
    disp.blit(bkgd, (rel - bkgd.get_rect().width, 0))

    if rel < 1600:
        disp.blit(bkgd, (rel, 0))

    scroll += 2

    pygame.display.update()

    pygame.event.pump()

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
