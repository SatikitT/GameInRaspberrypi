import sys
import threading
from settings import *
from server import Server
from cache import Cache
from player import Player
from scene import Scene
from menu import Menu

class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0.01
        self.maximum_lap = 3
        self.game_state = 'menu'
        
        # Time interval for updating other players (in milliseconds)
        self.update_interval = 100  # Update every 1000 ms (1 second)
        self.last_update_time = pg.time.get_ticks()  # Initialize last update time

        # Groups
        self.main_group = pg.sprite.LayeredUpdates()
        self.collision_group = pg.sprite.Group()
        self.finishline_group = pg.sprite.Group()
        self.transparent_objects = []
        
        # Game objects
        self.cache = Cache()
        self.player = Player(self)
        self.scene = Scene(self)
        self.menu = Menu(self)

        # Network
        self.server = Server(self)

    def update(self):
        self.scene.update()
        self.main_group.update()

        current_time = pg.time.get_ticks()
        if current_time - self.last_update_time >= self.update_interval:
            self.server.update_pos(self.player.offset, self.player.angle)
            self.server.load_other_players()
            self.last_update_time = current_time 

        if self.player.lap >= self.maximum_lap:
            self.game_state = 'menu'

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
                self.server.disconnect_from_server()
                self.game_state = 'menu'
                

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        while True:
            match (self.game_state):
                case 'menu':
                    self.menu.run()
                    self.player.lap = -1
                case 'start':
                    self.check_events()
                    self.get_time()
                    self.update()
                    self.draw()
                case _:
                    pg.quit()
                    sys.exit()
                    break

if __name__ == '__main__':
    app = App()
    app.run()
