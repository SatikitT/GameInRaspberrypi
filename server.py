import socket
import pickle
from stacked_sprite import vec2, StackedSprite
#'57.155.64.75'
class Server:
    def __init__(self, app):
        self.hostname = '57.155.64.75'
        self.port = 8080
        self.client_socket = None
        self.app = app
        self.player_name = None
        self.other_players_sprites = []
        self.game_running = True  # Track game state

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.hostname, self.port))
            
            # Receive the assigned player name from the server
            data = self.client_socket.recv(4096)
            self.player_name, self.app.player.offset.x, self.app.player.offset.y = pickle.loads(data)
            
            print(f"Connected to server as {self.player_name}")
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def update_pos(self, pos: vec2, angle: float):
        """Send player's position data to the server."""
        if not self.client_socket or not self.game_running:
            print("Game over or not connected.")
            return
        try:
            data = (self.player_name, pos.x, pos.y, angle)
            self.client_socket.sendall(pickle.dumps(data))
        except Exception as e:
            print(f"Error sending position data: {e}")

    def send_win_notification(self):
        """Notify the server that this player has won."""
        if self.client_socket:
            try:
                self.client_socket.sendall(pickle.dumps("WIN"))
                print("Sent win notification to the server.")
            except Exception as e:
                print(f"Error sending win notification: {e}")

    def load_other_players(self):
        """Receive other players' positions from the server."""
        if not self.game_running:
            return
        try:
            data = self.client_socket.recv(4096)
            if data:
                message = pickle.loads(data)
                
                # Handle stop or win/loss messages
                if message == "STOP":
                    print("Game over.")
                    self.game_running = False
                    return
                elif isinstance(message, str):
                    print(message)  # Display win/lose message
                    self.game_running = False
                    return
                
                # Deserialize player data if it's a regular update
                for _, (player_name, x, y, angle) in message.items():
                    pos = vec2(x, y)
                    if player_name != self.player_name:
                        # Find or create sprite for the player
                        existing_sprite = next((s for s in self.other_players_sprites if s.name == player_name), None)
                        if existing_sprite:
                            existing_sprite.pos = pos
                            existing_sprite.rot = angle * 23
                        else:
                            sprite = StackedSprite(self.app, name='car', pos=pos)
                            sprite.name = player_name
                            self.other_players_sprites.append(sprite)

        except Exception as e:
            print(f"Error receiving other players' data: {e}")

    def disconnect_from_server(self):
        if self.client_socket:
            self.client_socket.close()
        print("Disconnected from the server.")
