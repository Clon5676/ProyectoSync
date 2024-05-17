
# import socket
# import argparse
# import time

# # # Constantes
# # SERVER_ADDRESS = "localhost"
# # SERVER_PORT = 8087
# # FOLDER_PATH = "..\ProyectoSync"
 

# #FOLDER_PATH = "..\ProyectoSync" 


# # Parse command-line arguments
# parser = argparse.ArgumentParser(description="Client for folder scanning on a remote server.")
# parser.add_argument("server_address", help="Server address (IP or hostname)")
# parser.add_argument("port", type=int, help="Port number on the server")
# parser.add_argument("folder_path", help="Path to the folder to be scanned")
# args = parser.parse_args()

# # Server configuration
# SERVER_ADDRESS = args.server_address
# SERVER_PORT = args.port
# FOLDER_PATH = args.folder_path


# # Crear un socket y conectarse al servidor
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

# # Enviar el mensaje al servidor
# client_socket.send(f"LIST {FOLDER_PATH}".encode())

# # Recibir la respuesta del servidor
# response = client_socket.recv(1024).decode()
# print("Server response:", response)

# # Recibir el contenido del folder
# folder_content = client_socket.recv(1024).decode()
# print("Folder content:", folder_content)

# # Cerrar la conexión con el servidor
# client_socket.close()

import socket
import argparse
import time

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Client for folder scanning on a remote server.")
parser.add_argument("server_address", help="Server address (IP or hostname)")
parser.add_argument("port", type=int, help="Port number on the server")
parser.add_argument("folder_path", help="Path to the folder to be scanned")
args = parser.parse_args()

<<<<<<< HEAD
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
            return self.path_to_scan  # Add this line to return the path
=======
# Server configuration
SERVER_ADDRESS = args.server_address
SERVER_PORT = args.port
FOLDER_PATH = args.folder_path

# Crear un socket y conectarse al servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
>>>>>>> parent of f21acf2 (codigo final)

# Enviar el mensaje al servidor
client_socket.send(f"LIST {FOLDER_PATH}".encode())

<<<<<<< HEAD
    client = Client(server_ip, server_port, path_to_scan)
    path_taken = client.start()
    print(f'The path taken was: {path_taken}')
=======
# Recibir la respuesta del servidor
response = client_socket.recv(1024).decode()
print("Server response:", response)

# Recibir el contenido del folder
folder_content = client_socket.recv(1024).decode()
print("Folder content:", folder_content)

# Cerrar la conexión con el servidor
client_socket.close()
>>>>>>> parent of f21acf2 (codigo final)
