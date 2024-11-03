import pygame as pg
import math
import time
from settings import *

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
        self.angle = 0
        self.diag_move_corr = 1 / math.sqrt(2)

        self.attrs = STACKED_SPRITE_ATTRS[name]
        self.cache = app.cache.stacked_sprite_cache
        self.viewing_angle = app.cache.viewing_angle
        self.rotated_sprites = self.cache[name]['rotated_sprites']

        self.last_update_time = time.time()  # Track the last update time
        self.update_interval = 0.1  # Update every 100 ms

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

        current_time = time.time()
        if current_time - self.last_update_time >= self.update_interval:
            player_name = 'Player1'
            new_position = {"x": self.offset[0], "y": self.offset[1]}
            self.app.server.update_player_position(player_name, new_position)
            self.last_update_time = current_time  # Reset the last update time

    def move(self):
        self.offset += self.inc

    def get_image(self):
        frame = math.degrees(self.angle) % 360
        frame = int(frame / (360 / NUM_ANGLES))

        self.image = self.rotated_sprites[frame]
        self.rect = self.image.get_rect(center=self.rect.center)
