import pygame
import spritelings
import controllers
import missiles

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


class player(spritelings.actor):
    def __init__(self, pos):
        super().__init__(spritesheet, pos)

        self.hp = 100
        self.max_focus = 150
        self.focus = 0
        self.cooldwon = 0

        self.torso = {(0,0):neutral, (1,0):right, (1,-1):top_right, (1,1):bottom_right, (0,-1):top,
                      (0,1):down, (-1,0):left, (-1,-1):top_left, (-1,1):bottom_left}

        self.image = neutral
        self.rect = self.image.get_rect()

        center = self.rect.center
        self.hitbox = self.rect.inflate(-20, -39)
        self.hitbox.center = center


        self.facing = (0,0)
        self.velocity = (0,0)
        self.speed = 8

        self.controller = controllers.keyboard(self)

        self.spellbook = {1:missiles.kinetic_bolt, 2:missiles.acid_bolt, 3:missiles.fire_bolt, 4:missiles.ice_bolt, 5:missiles.acid_blast}
        self.page = 1
        self.spell = self.spellbook[1](self)

    def update(self, room):
        if self.hp <= 0:
            self.kill()

        self.controller.update(room)
        self.check_state()
        room.inactivePlayerProjectiles.add(self.spell)

        self.image = self.torso[self.facing]

        self.rect.move_ip(self.velocity)
        self.hitbox.center = self.rect.center

    def next_spell(self):
        if self.page < len(self.spellbook):
            self.spell.kill()
            self.page += 1
            self.spell = self.spellbook[self.page](self)

    def prev_spell(self):
        if self.page > 1:
            self.spell.kill()
            self.page -= 1
            self.spell = self.spellbook[self.page](self)

    def cast(self, room):
        self.spell.fire(self.facing, room)
        self.spell = self.spellbook[self.page](self)

    def anim(self):
        pass



