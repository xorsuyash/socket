import socket 
import sys 
import os 

PORT=5050
HEADER=64
FORMAT="utf-8"
SERVER= socket.gethostbyname(socket.gethostname())
DISCONNECT="!Disconnect"
ADDR=(SERVER,PORT)
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(ADDR)

def send(msg):
    message=msg.encode(FORMAT)
    msg_length=len(message)
    send_length=str(msg_length).encode(FORMAT)
    send_length+=b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def send_file(filename):
    with open(filename, 'rb') as file:
        file_data = file.read()
        send(f"!file {os.path.basename(filename)}")
        send(len(file_data))
        client.send(file_data)
        print(f"File '{filename}' sent successfully.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 client.py <FILE PATH>")
        return

    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return


    # Create a new socket and connect to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    try:
        client.connect(ADDR)
    except OSError as e:
        print(f"Error connecting to the server: {e}")
        return

    # Send the file
    send_file(filepath)

    # Receive acknowledgment
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        print(msg)

    # Disconnect
    send(DISCONNECT)

if __name__ == "__main__":
    main()

