# import paramiko
# import re
# from stacked_sprite import vec2, StackedSprite

# class Server:
#     def __init__(self, app):
#         self.hostname = '192.168.1.167'
#         self.username = 'user'
#         self.password = 'password'
#         self.ssh = None
#         self.sftp = None
#         self.app = app
#         self.player_name = None
#         self.remote_directory = "test"
#         self.other_players_sprites = []

#     def connect_to_server(self):
#         try:
#             ssh = paramiko.SSHClient()
#             ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#             ssh.connect(self.hostname, username=self.username, password=self.password)
#             self.ssh = ssh
#             self.sftp = ssh.open_sftp()  # Open SFTP session
#             print("server connected")
#         except Exception as e:
#             print(f"error connect server: {e}")

#     def create_player_file(self):
#         try:
#             files = self.sftp.listdir(self.remote_directory)
            
#             numbers = [
#                 int(re.match(r"(\d+)\.txt", file).group(1))
#                 for file in files
#                 if re.match(r"(\d+)\.txt", file)
#             ]

#             next_number = max(numbers) + 1 if numbers else 1
#             new_file_path = f"{self.remote_directory}/{next_number}.txt"
            
#             with self.sftp.file(new_file_path, 'w') as remote_file:
#                 remote_file.write("")
#                 print(f"created file {new_file_path}")
#             self.player_name = new_file_path

#         except Exception as e:
#             print(f"error create file: {e}")

#     def update_pos(self, pos: vec2):
#         try:
#             if not self.player_name:
#                 print("player name not found")
#                 return
            
#             with self.sftp.file(self.player_name, 'w') as f:
#                 f.write(f"{int(pos.x)},{int(pos.y)}")
#                 #print(f"Updated position for {self.player_name} to ({pos.x}, {pos.y})")
                
#         except Exception as e:
#             print(f"Error updating position: {e}")

#     def load_other_players(self):
#         """Load or update other players' positions from their files and instantiate or update their sprites."""
#         try:
#             files = self.sftp.listdir(self.remote_directory)

#             for file in files:
#                 file_path = f"{self.remote_directory}/{file}"
                
#                 # Skip the player's own file
#                 if file_path == self.player_name:
#                     continue
                
#                 # Read position data for each other player
#                 with self.sftp.file(file_path, 'r') as f:
#                     content = f.read().decode('utf-8').strip()
#                     if content:
#                         x, y = content.split(",")
#                         pos = vec2(int(x), int(y))
                        
#                         # Check if this player already has a sprite
#                         existing_sprite = next((sprite for sprite in self.other_players_sprites if sprite.file_path == file_path), None)
                        
#                         if existing_sprite:
#                             # Update position if sprite already exists
#                             existing_sprite.pos = pos
#                             print(f"Updated other player sprite from {file_path} to new position ({x}, {y})")
#                         else:
#                             # Create a new sprite if it doesn't exist
#                             sprite = StackedSprite(self.app, name='car', pos=pos)
#                             sprite.file_path = file_path  # Add file path for easier identification
#                             self.other_players_sprites.append(sprite)
#                             print(f"Loaded new other player sprite from {file_path} at position ({x}, {y})")

#         except Exception as e:
#             print(f"Error loading or updating other players: {e}")

#     def delete_player_file(self):
#         """Delete the player's file from the server."""
#         try:
#             if self.player_name:
#                 self.sftp.remove(self.player_name)
#                 print(f"Deleted player file: {self.player_name}")
#         except Exception as e:
#             print(f"Error deleting player file: {e}")

#     def disconnect_from_server(self):
#         """Close SFTP and SSH connection."""
#         self.delete_player_file()
#         if self.sftp:
#             self.sftp.close()
#         if self.ssh:
#             self.ssh.close()
#         print("Disconnected from the server.")
# server.py
import socket
import pickle
from stacked_sprite import vec2, StackedSprite

class Server:
    def __init__(self, app):
        self.hostname = '192.168.1.167'
        self.port = 5555
        self.client_socket = None
        self.app = app
        self.player_name = f"player_{id(self)}"
        self.other_players_sprites = []

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.hostname, self.port))
            print("Server connected")
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
            print(f"Sent position for {self.player_name}: ({pos.x}, {pos.y})")
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
                        # Find or create sprite for the player
                        existing_sprite = next((sprite for sprite in self.other_players_sprites if sprite.name == player_name), None)
                        if existing_sprite:
                            existing_sprite.pos = pos
                            existing_sprite.rot = angle * 23
                        else:
                            # Create a new sprite if not found
                            sprite = StackedSprite(self.app, name='car', pos=pos)
                            sprite.name = player_name
                            self.other_players_sprites.append(sprite)

                print(f"Updated players: {players_data}")

        except Exception as e:
            print(f"Error receiving other players' data: {e}")

    def disconnect_from_server(self):
        """Disconnect from the server."""
        if self.client_socket:
            self.client_socket.close()
        print("Disconnected from the server.")
