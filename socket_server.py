import socket
import json
from datetime import datetime

HOST = 'localhost'
PORT = 5000

def save_to_json(data):
    with open('storage/data.json', 'a') as file:
        json.dump(data, file, indent=2)
        file.write('\n')

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((HOST, PORT))
        print(f'Socket server is running on {HOST}:{PORT}')

        while True:
            data, addr = server_socket.recvfrom(1024)
            data = data.decode('utf-8')
            message = json.loads(data)
            message['timestamp'] = str(datetime.now())
            save_to_json(message)
            print(f"Received message from {addr}: {message}")

if __name__ == "__main__":
    main()
