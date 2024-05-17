import socket
import sys
import time
import os

class Client:
    def __init__(self, server_ip, server_port, path_to_scan):
        self.server_ip = server_ip
        self.server_port = server_port
        self.path_to_scan = path_to_scan

    def get_files_in_path(self, path):
        files = os.listdir(path)
        return files

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            print(f'Connecting to {self.server_ip}:{self.server_port}')
            client_socket.connect((self.server_ip, self.server_port))
            print(client_socket.recv(1024).decode())
            while True:
                print(f'Sending path to scan: {self.path_to_scan}')
                client_socket.sendall(self.path_to_scan.encode())
                response = client_socket.recv(1024).decode()
                print(response)
                if 'Request accepted' in response:
                    break
                time.sleep(1)
            files_in_path = self.get_files_in_path(self.path_to_scan)
            return files_in_path

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: client.py <server_ip> <server_port> <path_to_scan>')
        sys.exit(1)
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    path_to_scan = sys.argv[3]

    client = Client(server_ip, server_port, path_to_scan)
    files_found = client.start()
    print(f'The files found in the path are: {files_found}')