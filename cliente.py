
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

# Server configuration
SERVER_ADDRESS = args.server_address
SERVER_PORT = args.port
FOLDER_PATH = args.folder_path

# Crear un socket y conectarse al servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

# Enviar el mensaje al servidor
client_socket.send(f"LIST {FOLDER_PATH}".encode())

# Recibir la respuesta del servidor
response = client_socket.recv(1024).decode()
print("Server response:", response)

# Recibir el contenido del folder
folder_content = client_socket.recv(1024).decode()
print("Folder content:", folder_content)

# Cerrar la conexión con el servidor
client_socket.close()