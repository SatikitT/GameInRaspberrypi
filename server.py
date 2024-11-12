import socket
import pickle
from stacked_sprite import vec2, StackedSprite

# self.hostname = '57.155.64.75'
# self.port = 8080

class Server:
    def __init__(self, app):
        self.hostname = '57.155.64.75'
        self.port = 8080
        self.client_socket = None
        self.app = app
        self.player_name = None
        self.other_players_sprites = []

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.hostname, self.port))
            
            data = self.client_socket.recv(4096)
            print(pickle.loads(data))
            self.player_name, self.app.player.offset.x, self.app.player.offset.y = pickle.loads(data)
            
            print(f"Connected to server as {self.player_name}")
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def update_pos(self, pos: vec2, angle: float):
        """Send player's position data to the server."""
        try:
            if not self.client_socket:
                print("Not connected to server")
                return
            # Send serialized position data as a tuple (player name, x, y)
            data = (self.player_name, pos.x, pos.y, angle)
            self.client_socket.sendall(pickle.dumps(data))
            #print(f"Sent position for {self.player_name}: ({pos.x}, {pos.y})")
        except Exception as e:
            print(f"Error sending position data: {e}")

    def load_other_players(self):
        """Receive other players' positions from the server."""
        try:
            # Receive serialized data from server
            data = self.client_socket.recv(4096)
            if data:
                # Deserialize the data
                players_data = pickle.loads(data)

                for _, (player_name, x, y, angle) in players_data.items():
                    pos = vec2(x, y)
                    if (player_name != self.player_name):
                        existing_sprite = next((sprite for sprite in self.other_players_sprites if sprite.name == player_name), None)
                        if existing_sprite:
                            if existing_sprite.pos == vec2(-1,-1):
                                existing_sprite.kill()
                                self.app.menu.winner = existing_sprite.name + " won"
                                self.app.game_state = 'menu'
                            elif existing_sprite.pos == vec2(-2,-2):
                                existing_sprite.kill()
                            existing_sprite.pos = pos
                            existing_sprite.rot = angle * 23
                        else:
                            # Create a new sprite if not found
                            sprite = StackedSprite(self.app, name='car', pos=pos)
                            sprite.name = player_name
                            print(f"create {sprite.name}")
                            self.other_players_sprites.append(sprite)
                            
        except Exception as e:
            print(f"Error receiving other players' data: {e}")

    def disconnect_from_server(self):
        """Disconnect from the server."""
        if self.client_socket:
            self.client_socket.close()
        print("Disconnected from the server.")
