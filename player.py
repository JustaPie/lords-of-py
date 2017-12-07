import pygame

import controllers
import missiles
import spritelings

spritesheet = pygame.image.load('people\smol_silvia.png').convert_alpha()
neutral = spritesheet.subsurface((0,0), (59,126))
right = spritesheet.subsurface((60,0), (67,126))
top_right = spritesheet.subsurface((128, 0), (58, 126))
bottom_right = spritesheet.subsurface((187,0), (67,126))
left = pygame.transform.flip(right, 1, 0)
top_left = pygame.transform.flip(top_right, 1, 0)
bottom_left = pygame.transform.flip(bottom_right, 1, 0)
down = spritesheet.subsurface((257,0), (38,126))
top = spritesheet.subsurface((299, 0), (38,126))

shot = pygame.mixer.Sound("audio/burst_laser.wav")
died = pygame.mixer.Sound("audio/player_death.wav")
ow = pygame.mixer.Sound("audio/ow.wav")
swap = pygame.mixer.Sound("audio/spell_swap.wav")
died.set_volume(1)
class player(spritelings.actor):
    def __init__(self, pos, original = None):
        super().__init__(spritesheet, pos)

        self.hp = 100
        self.max_focus = 150
        self.focus = 0
        self.charge_level = 1

        self.torso = {(0,0):neutral, (1,0):right, (1,-1):top_right, (1,1):bottom_right, (0,-1):top,
                      (0,1):down, (-1,0):left, (-1,-1):top_left, (-1,1):bottom_left}

        self.image = neutral
        self.rect = self.image.get_rect()

        center = self.rect.center
        self.hitbox = self.rect.inflate(-20, -39)
        self.hitbox.center = center
        self.hitboxes = [self.hitbox]


        self.facing = (0,0)
        self.velocity = (0,0)
        self.speed = 8

        self.controller = controllers.auto(self)

        self.spellbook = {1:missiles.acid_bolt, 2:missiles.freezing_burst, 3:missiles.fire_bolt, 4:missiles.ice_bolt, 5:missiles.lava_burst, 6:missiles.kinetic_splitter}
        self.page = 1
        self.spell = self.spellbook[1](self)

    def update(self, room):
        if self.hp <= 0:
            self.spell.kill()
            self.kill()
            died.play()


        self.controller.update(room)
        room.inactivePlayerProjectiles.add(self.spell)

        self.image = self.torso[self.facing]

        self.rect.move_ip(self.velocity)
        self.hitbox.center = self.rect.center
        self.spell.rect.center = self.rect.center

    def next_spell(self):
        if self.page < len(self.spellbook):
            self.spell.kill()
            self.page += 1
            self.spell = self.spellbook[self.page](self)
            swap.play()

    def prev_spell(self):
        if self.page > 1:
            self.spell.kill()
            self.page -= 1
            self.spell = self.spellbook[self.page](self)
            swap.play()

    def cast(self, room):
        self.spell.fire(self.facing, room.playerProjectiles)
        self.spell = self.spellbook[self.page](self)
        shot.play()

    def anim(self):
        pass

    def react(self, bastard):
        print(type(bastard))
        self.rect.move_ip(bastard.knockback)
        self.hp -= bastard.damage
        ow.play()
        self.spell.kill()
        if isinstance(bastard, missiles.missile):
            bastard.kill()




