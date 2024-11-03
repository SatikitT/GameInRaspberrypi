import socket
from _thread import *
import sys

server = "192.168.1.83"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connection")

def threaded_client(conn):
    reply = ""
    while True:
        try: 
            data = conn.recv(2048)

            if not data:
                print("Disconnected")
                break

            reply = data.decode("utf-8")
            print("Received:", reply)
            conn.sendall(reply.encode("utf-8"))
            print("Sent:", reply)
            
        except:
            break

    print("Lost connection")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connect to", addr)

    start_new_thread(threaded_client, (conn, ))
    