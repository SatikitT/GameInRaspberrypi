import paramiko
import json
import threading
import time

class Server:
    def __init__(self):
        self.hostname = '161.246.5.62'
        self.username = 'u66011215'
        self.password = 'Papika528'
        self.player_data = {}
        self.update_interval = 0.1 
        self.stop_thread = False 
        self.ssh = None  
        self.thread = None 
        self.player_name = "Player1"

    def connect_to_server(self):
        """Establish an SSH connection to the server."""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.hostname, username=self.username, password=self.password)
            self.ssh = ssh  # Save the connection
            print("Connected to the server.")
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def update_player_position(self, player_name, new_position):
        """Update the player's position in memory and on the server."""
        if player_name in self.player_data:
            self.player_data[player_name]['position'] = new_position
            print(f"Updated position for {player_name} to {new_position}.")
        else:
            print(f"Player {player_name} not found. Creating a new player.")
            self.player_data[player_name] = {'position': new_position}  # Create new entry if not found
            print(f"Created a new entry for {player_name}.")

    def read_file(self, remote_file_path):
        """Read player data from the remote file and create a player if not found."""
        try:
            sftp = self.ssh.open_sftp()
            with sftp.file(remote_file_path, 'r') as file:
                data = file.read()
                self.player_data = json.loads(data.decode('utf-8'))  # Store data in memory

            # Check if the player exists in the loaded data
            if self.player_name not in self.player_data:
                print(f"Player {self.player_name} not found in the data. Creating a new player.")
                self.player_data[self.player_name] = {'position': {'x': 0, 'y': 0}}  # Create a new player entry
                self.write_file(remote_file_path)  # Write the new player to the file
            else:
                print("Player data read successfully.")
        except Exception as e:
            print(f"Error reading file: {e}")
        finally:
            sftp.close()

    def write_file(self, remote_file_path):
        """Write player data to the remote file."""
        try:
            with self.ssh.open_sftp() as sftp:
                with sftp.file(remote_file_path, 'w') as file:
                    file.write(json.dumps(self.player_data))  # Write all data at once
                    print(f"File {remote_file_path} updated successfully.")
        except Exception as e:
            print(f"Error writing file: {e}")

    def delete_player(self, remote_file_path):
        """Remove the player from the JSON file."""
        if self.player_name in self.player_data:
            del self.player_data[self.player_name]  # Remove the player from memory
            self.write_file(remote_file_path)  # Update the remote file
            print(f"Deleted player {self.player_name} from the server.")

    def start_updating(self, remote_file_path):
        """Start a thread to periodically update the player positions."""
        if self.ssh is None:
            self.connect_to_server()  # Ensure connection is established
        self.read_file(remote_file_path)  # Initial read
        
        self.stop_thread = False  # Reset the stop flag

        # Define the thread target function
        def update_loop():
            while not self.stop_thread:
                self.write_file(remote_file_path)  # Write data periodically
                time.sleep(self.update_interval)  # Control update frequency
        
        self.thread = threading.Thread(target=update_loop)
        self.thread.start()  # Start the updating thread
        print("Started updating thread.")

    def stop_updating(self):
        """Stop the updating thread."""
        self.stop_thread = True
        if self.thread is not None:
            self.thread.join()  # Wait for the thread to finish
            print("Updating thread stopped.")
        if self.ssh:
            self.ssh.close()  # Close the SSH connection
            print("SSH connection closed.")
