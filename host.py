import socket
import threading
import pickle
import uuid  # For unique player IDs

# Server configuration
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 5555

# Dictionary to hold player positions
players = {}
connections = []  # List to hold client connections for broadcasting

# Lock for thread-safe access
lock = threading.Lock()

def handle_client(conn, player_id):
    with conn:
        print(f"Player {player_id} connected.")
        with lock:
            players[player_id] = (100, 100)  # Initial position
            connections.append(conn)

        try:
            while True:
                # Receive data from client
                data = conn.recv(4096)
                if not data:
                    break

                try:
                    # Deserialize position update from client
                    pos = pickle.loads(data)
                except pickle.PickleError:
                    print(f"Received corrupt data from {player_id}.")
                    break

                # Update the player's position
                with lock:
                    players[player_id] = pos

                    # Prepare and send the updated positions to all clients
                    player_data = pickle.dumps(players)

                    # Broadcast to all clients
                    for client_conn in connections:
                        try:
                            client_conn.sendall(player_data)
                        except (ConnectionResetError, ConnectionAbortedError):
                            print(f"Error sending data to a client. Removing client.")
                            connections.remove(client_conn)

        except (ConnectionResetError, ConnectionAbortedError):
            print(f"Player {player_id} disconnected abruptly.")
        except Exception as e:
            print(f"An error occurred with player {player_id}: {e}")
        finally:
            # Clean up the player on disconnection
            with lock:
                if player_id in players:
                    del players[player_id]
                if conn in connections:
                    connections.remove(conn)
            print(f"Player {player_id} removed.")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            player_id = str(uuid.uuid4())  # Unique player ID using UUID
            # Start a new thread for each client
            threading.Thread(target=handle_client, args=(conn, player_id), daemon=True).start()

if __name__ == "__main__":
    start_server()
