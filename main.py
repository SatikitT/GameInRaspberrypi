import sys
import threading
from settings import *
from server import Server
from cache import Cache
from player import Player
from scene import Scene
from menu import Menu
import threading
import serial




class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0.01
        self.maximum_lap = 3
        self.game_state = 'menu'

        self.serial_data = {"gas": 0, "brake": 0, "wheel": 0}
        self.update_interval = 100  # Update every 1000 ms (1 second)
        self.last_update_time = pg.time.get_ticks()  # Initialize last update time

        self.main_group = pg.sprite.LayeredUpdates()
        self.collision_group = pg.sprite.Group()
        self.finishline_group = pg.sprite.Group()
        self.transparent_objects = []
        
        self.cache = Cache()
        self.player = Player(self)
        self.scene = Scene(self)
        self.menu = Menu(self)

        
        threading.Thread(target=self.serial_reader, daemon=True).start()
        # self.server = Server(self)

    def serial_reader(self):
        ser = serial.Serial('COM5', 115200, timeout=1)  # Replace COMx with your port

        while True:
            line = ser.readline().decode().strip()
            print(line)
            if line.startswith("Gas:"):
                try:
                    parts = line.split(',')
                    self.serial_data["gas"] = int(parts[0].split(":")[1].strip())
                    self.serial_data["brake"] = int(parts[1].split(":")[1].strip())
                    self.serial_data["wheel"] = int(parts[2].split(":")[1].strip())
                except Exception as e:
                    print(f"Parse error: {e} | Line: {line}")

    def update(self):
        self.scene.update()
        self.main_group.update()

        current_time = pg.time.get_ticks()
        if current_time - self.last_update_time >= self.update_interval:
            # self.server.update_pos(self.player.offset, self.player.angle)
            # self.server.load_other_players()
            self.last_update_time = current_time 

        if self.player.lap >= self.maximum_lap:
            # self.server.update_pos(vec2(-1, -1), 0)
            # self.server.load_other_players()
            # self.menu.winner = self.server.player_name + " won"
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
                # self.server.update_pos(vec2(-2, -2), 0)
                self.game_state = 'menu'

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        while True:
            match (self.game_state):
                case 'menu':
                    self.menu.run()
                    self.player.lap = -1
                    # for sprite in self.server.other_players_sprites:
                    #     sprite.kill()
                case 'start':
                    self.check_events()
                    self.get_time()
                    self.draw()
                    self.update()
                case _:
                    pg.quit()
                    sys.exit()
                    break

if __name__ == '__main__':
    app = App()
    app.run()
