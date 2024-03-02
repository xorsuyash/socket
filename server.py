import socket 
import threading 

PORT=5050
HEADER=64
FORMAT="utf-8"
SERVER= socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
DISCONNECT="!Disconnect"
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT:
                connected = False
            elif msg.startswith("!file "):
                filename = msg.split(" ")[1]
                receive_file(conn, filename)
            else:
                print(f"{addr}: {msg}")
                conn.send("Msg received".encode(FORMAT))
    
    conn.close()

def receive_file(conn, filename):
    file_size = int(conn.recv(HEADER).decode(FORMAT))
    with open(filename, 'wb') as file:
        data = conn.recv(file_size)
        file.write(data)
        print(f"File '{filename}' received successfully.")

def start():
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting")
start()


