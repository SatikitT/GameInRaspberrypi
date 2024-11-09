import pygame as pg
import math
from settings import *

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Player(pg.sprite.Sprite):
    def __init__(self, app, name='car'):
        self.app = app
        self.group = app.main_group
        super().__init__(self.group)

        self.group.change_layer(self, CENTER.y)

        size = vec2([50, 50])
        self.image = pg.Surface(size, pg.SRCALPHA)
        self.rect = self.image.get_rect(center=CENTER)

        self.offset = vec2(0)
        self.inc = vec2(0)
        self.prev_inc = vec2(0)
        self.angle = 3.14/2
        self.diag_move_corr = 1 / math.sqrt(2)

        self.attrs = STACKED_SPRITE_ATTRS[name]
        self.cache = app.cache.stacked_sprite_cache
        self.viewing_angle = app.cache.viewing_angle
        self.rotated_sprites = self.cache[name]['rotated_sprites']
        
        self.name = ""

    def set_name(self, name: str):
        self.name = name

    def control(self):

        self.inc = vec2(0)
        speed = PLAYER_SPEED * self.app.delta_time
        rot_speed = PLAYER_ROT_SPEED * self.app.delta_time
        

        key_state = pg.key.get_pressed()
        
        if key_state[pg.K_LEFT]:
            self.angle += rot_speed
        if key_state[pg.K_RIGHT]:
            self.angle += -rot_speed
    
        if key_state[pg.K_w]:
            self.inc.x += speed * math.sin(self.angle * 2)
            self.inc.y += speed * math.cos(self.angle * 2)

        if key_state[pg.K_s]:
            self.inc.x -= speed * math.sin(self.angle * 2)
            self.inc.y -= speed * math.cos(self.angle * 2)

        if self.inc.x and self.inc.y:
            self.inc *= self.diag_move_corr

    def check_collision(self):
        hit = pg.sprite.spritecollide(self, self.app.collision_group,
                                      dokill=False, collided=pg.sprite.collide_mask)
        if not hit:
            if self.inc.x or self.inc.y:
                self.prev_inc = self.inc
        else:
            self.inc = -self.prev_inc

    def update(self):
        self.control()
        self.check_collision()
        self.get_image()
        self.move()

    def move(self):
        self.offset += self.inc

    def get_image(self):
        frame = math.degrees(self.angle) % 360
        frame = int(frame / (360 / NUM_ANGLES))

        self.image = self.rotated_sprites[frame]
        self.rect = self.image.get_rect(center=self.rect.center)
