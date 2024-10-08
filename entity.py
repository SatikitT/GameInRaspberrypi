from settings import *


class BaseEntity(pg.sprite.Sprite):
    def __init__(self, app, name):
        self.app = app
        self.name = name
        self.group = app.main_group
        super().__init__(self.group)

        self.attrs = STACKED_SPRITE_ATTRS[name]
        self.cache = app.cache.stacked_sprite_cache
        self.viewing_angle = app.cache.viewing_angle
        self.rotated_sprites = self.cache[name]['rotated_sprites']
        self.collision_masks = self.cache[name]['collision_masks']

    def update(self):
        pass

    def get_image(self):
        self.image = self.rotated_sprites[self.angle]
        self.mask = self.collision_masks[self.angle]
        self.rect = self.image.get_rect(center=self.screen_pos + self.y_offset)


class Entity(BaseEntity):
    def __init__(self, app, name, pos):
        super().__init__(app, name)
        self.pos = vec2(pos) * TILE_SIZE
        self.player = app.player
        self.y_offset = vec2(0, self.attrs['y_offset'])
        self.screen_pos = vec2(0)

    def update(self):
        super().update()
        self.transform()
        self.set_rect()
        self.change_layer()

    def transform(self):
        pos = self.pos - self.player.offset
        pos = pos.rotate_rad(self.player.angle)
        self.screen_pos = pos + CENTER

    def change_layer(self):
        self.group.change_layer(self, self.screen_pos.y)

    def set_rect(self):
        self.rect.center = self.screen_pos + self.y_offset


















