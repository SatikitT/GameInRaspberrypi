import socket
import threading
import pickle
import uuid  # For unique player IDs

# Server configuration
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 8080

# Dictionary to hold player positions and angles
players = {}
connections = []  # List to hold client connections for broadcasting

# Lock for thread-safe access
lock = threading.Lock()

def handle_client(conn):
    with conn:
        # Generate a unique player name based on UUID
        player_name = f"player_{str(uuid.uuid4())[:8]}"
        print(f"{player_name} connected.")

        # Send the player name and initial position to the client
        initial_x = 175 + 100 * len(connections)
        initial_y = 750
        conn.sendall(pickle.dumps((player_name, initial_x, initial_y)))

        with lock:
            # Initialize player with default position and angle
            players[player_name] = (player_name, initial_x, initial_y, 0)  # (player_name, x, y, angle)
            connections.append(conn)

        try:
            while True:
                data = conn.recv(4096)
                if not data:
                    break

                try:
                    # Deserialize position update from client
                    _, x, y, angle = pickle.loads(data)  # Ignore the client-sent name
                except pickle.PickleError:
                    print(f"Received corrupt data from {player_name}.")
                    break

                # Update the player's position and angle on the server
                with lock:
                    players[player_name] = (player_name, x, y, angle)

                    # Broadcast updated player data to all clients
                    player_data = pickle.dumps(players)
                    for client_conn in connections:
                        try:
                            client_conn.sendall(player_data)
                        except (ConnectionResetError, ConnectionAbortedError):
                            connections.remove(client_conn)

        finally:
            # Clean up on disconnection
            with lock:
                if player_name in players:
                    del players[player_name]
                if conn in connections:
                    connections.remove(conn)
            print(f"{player_name} removed.")


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            # Start a new thread for each client
            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    start_server()
