import sys
import pygame as pg
from settings import *
from server import Server
from cache import Cache
from player import Player
from scene import Scene

class App:
    def __init__(self):
        pg.init()  # Initialize Pygame
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0.01
        
        # Groups
        self.main_group = pg.sprite.LayeredUpdates()
        self.collision_group = pg.sprite.Group()
        self.transparent_objects = []
        
        # Game objects
        self.cache = Cache()
        self.player = Player(self)
        self.scene = Scene(self)

        # Network
        self.server = Server()
        remote_file_path = "python_game_data/player_positions.json"
        self.server.start_updating(remote_file_path)

    def update(self):
        self.scene.update()
        self.main_group.update()
        pg.display.set_caption(f'{self.clock.get_fps(): .1f}')
        self.delta_time = self.clock.tick()

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.main_group.draw(self.screen)
        pg.display.flip()

    def check_events(self):
        pg.event.set_allowed([pg.QUIT, pg.K_w, pg.K_s, pg.K_ESCAPE])
        self.anim_trigger = False
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                remote_file_path = "python_game_data/player_positions.json"  # Path to the remote file
                self.server.delete_player(remote_file_path)  # Delete the player before quitting
                self.server.stop_updating()  # Stop updating before quitting
                pg.quit()
                sys.exit()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        while True:
            self.check_events()
            self.get_time()
            self.update()
            self.draw()

if __name__ == '__main__':
    app = App()
    app.run()
