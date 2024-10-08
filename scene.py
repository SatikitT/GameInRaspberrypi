from stacked_sprite import *
from random import uniform
from entity import Entity

P = 'player'
K = 'kitty'
A, B, C, D, E, F, G, H = 'van', 'tank', 'blue_tree', 'car', 'grass', 'crate', 'cup', 'pancake'

MAP = [
    [F, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F],
    [F, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F],
    [F, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F],
    [F, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F],
    [F, 0, 0, F, F, F, F, F, F, F, F, 0, 0, F],
    [F, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F],
    [F, 0, P, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F],
    [F, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F],
    [F, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F],
]

MAP_SIZE = MAP_WIDTH, MAP_HEIGHT = vec2(len(MAP), len(MAP[0]))
MAP_CENTER = MAP_SIZE / 2


class Scene:
    def __init__(self, app):
        self.app = app
        self.transform_objects = []
        self.load_scene()

    def load_scene(self):
        rand_rot = lambda: uniform(0, 360)
        rand_pos = lambda pos: pos + vec2(uniform(-0.1, 0.1))

        for j, row in enumerate(MAP):
            for i, name in enumerate(row):
                pos = vec2(i, j) + vec2(0.5)
                if name == 'player':
                    self.app.player.offset = pos * TILE_SIZE
                elif name:
                    StackedSprite(self.app, name=name, pos=rand_pos(pos))

    def get_closest_object_to_player(self):
        closest = sorted(self.app.transparent_objects, key=lambda e: e.dist_to_player)

    def transform(self):
        for obj in self.transform_objects:
            obj.rot = 30 * self.app.time

    def update(self):
        self.get_closest_object_to_player()
        self.transform()


# elif name == 'kitty':
#     Entity(self.app, name=name, pos=pos)
# elif name == 'blue_tree':
#     TrnspStackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
# elif name == 'grass':
#     StackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot(),
#                   collision=False)
# elif name == 'sphere':
#     obj = StackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
#     self.transform_objects.append(obj)




