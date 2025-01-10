import socket
import threading
import pickle
import uuid  


HOST = '0.0.0.0'  
PORT = 8080


players = {}
connections = []  


lock = threading.Lock()

def handle_client(conn):
    with conn:
        
        player_name = f"player_{str(uuid.uuid4())[:8]}"
        print(f"{player_name} connected.")

        
        initial_x = 175 + 100 * len(connections)
        initial_y = 750
        conn.sendall(pickle.dumps((player_name, initial_x, initial_y)))

        with lock:
            
            players[player_name] = (player_name, initial_x, initial_y, 0)  
            connections.append(conn)

        try:
            while True:
                data = conn.recv(4096)
                if not data:
                    break

                try:
                    
                    _, x, y, angle = pickle.loads(data)  
                except pickle.PickleError:
                    print(f"Received corrupt data from {player_name}.")
                    break

                
                with lock:
                    players[player_name] = (player_name, x, y, angle)

                    
                    player_data = pickle.dumps(players)
                    for client_conn in connections:
                        try:
                            client_conn.sendall(player_data)
                        except (ConnectionResetError, ConnectionAbortedError):
                            connections.remove(client_conn)

        finally:
            
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
            
            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    start_server()
