import socket

# Constantes
SERVER_ADDRESS = "localhost"
SERVER_PORT = 8087
FOLDER_PATH = "c:\\myfolder"

# Crear un socket y conectarse al servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

# Enviar el mensaje al servidor
client_socket.send(f"LIST {FOLDER_PATH}".encode())

# Recibir la respuesta del servidor
response = client_socket.recv(1024).decode()

# Procesar la respuesta
if response.startswith("Request accepted"):
    print("Request accepted. Waiting for response...")
    # Recibir el contenido del folder
    folder_content = client_socket.recv(1024).decode()
    print("Folder content:", folder_content)
else:
    print("Request not accepted")

# Cerrar la conexión con el servidor
client_socket.close()