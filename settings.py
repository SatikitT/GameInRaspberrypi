import pygame as pg

vec2 = pg.math.Vector2

RES = WIDTH, HEIGHT = vec2(1600, 900)
#RES = WIDTH, HEIGHT = vec2(1920, 1080)
CENTER = H_WIDTH, H_HEIGHT = RES // 2
TILE_SIZE = 100  #

PLAYER_SPEED = 1
PLAYER_ROT_SPEED = 0.002

BG_COLOR = 'olivedrab'  #
NUM_ANGLES = 72

ENTITY_SPRITE_ATTRS = {
}

STACKED_SPRITE_ATTRS = {
    'crate': {
        'path': 'assets/stacked_sprites/crate.png',
        'num_layers': 16,
        'scale': 5,
        'y_offset': 10,
    },
    'wheel': {
        'path': 'assets/stacked_sprites/wheel.png',
        'num_layers': 4,
        'scale': 5,
        'y_offset': 0,
    },
    'grass': {
        'path': 'assets/stacked_sprites/grass.png',
        'num_layers': 11,
        'scale': 7,
        'y_offset': 20,
        'outline': False,
    },
    'car': {
        'path': 'assets/stacked_sprites/car.png',
        'num_layers': 9,
        'scale': 5,
        'y_offset': 5,
    },
    'van': {
        'path': 'assets/stacked_sprites/van.png',
        'num_layers': 20,
        'scale': 6,
        'y_offset': 10,
    },
    'tank': {
        'path': 'assets/stacked_sprites/tank.png',
        'num_layers': 17,
        'scale': 8,
        'y_offset': 0,
        'mask_layer': 4,
    },
}


















