
# import socket
# import threading
# import queue
# import os
# import argparse

# # Parse command-line arguments
# parser = argparse.ArgumentParser(description="Server for folder scanning with buffer and threads.")
# parser.add_argument("port", type=int, help="Port number to listen on")
# parser.add_argument("buffer_size", type=int, help="Size of the limited buffer")
# parser.add_argument("threads", type=int, help="Number of threads to handle clients")
# args = parser.parse_args()

# # Server configuration
# SERVER_PORT = args.port
# BUFFER_SIZE = args.buffer_size
# MAX_THREADS = args.threads


# # # Constantes
# # BUFFER_SIZE = 4  # Tamaño del buffer
# # MAX_THREADS = 2  # Número máximo de hilos que pueden operar en paralelo
# # SERVER_PORT = 8087


# # Crear un buffer y un semáforo para controlar el acceso
# buffer = queue.Queue(BUFFER_SIZE)
# mutex = threading.Lock()
# notEmpty = threading.Semaphore(0)
# notFull = threading.Semaphore(BUFFER_SIZE)

# # Función para obtener el contenido de un folder
# def get_folder_content(folder_path):
#     try:
#         # Obtener el listado de archivos y carpetas en el folder
#         contents = os.listdir(folder_path)
        
#         # Construir el mensaje con el contenido del folder
#         message = "Folder content:\n"
#         for item in contents:
#             item_path = os.path.join(folder_path, item)
#             if os.path.isdir(item_path):
#                 message += f"[DIR] {item}\n"
#             else:
#                 message += f"[FILE] {item}\n"
        
#         return message
    
#     except OSError as e:
#         # Manejar errores al acceder al folder
#         return f"Error accessing folder: {e}"

# # Función para manejar los clientes
# def handle_client(client_socket):
#     # Recibir el mensaje del cliente
#     message = client_socket.recv(1024).decode()
    
#     # Procesar el mensaje
#     if message.startswith("LIST"):
#         folder_path = message.split()[1]
        
#         # Verificar si hay espacio en el buffer
#         if notFull._value > 0:
#             # Agregar el mensaje al buffer
#             buffer.put(message)
#             notFull._value -= 1
#             notEmpty._value += 1
            
#             # Obtener el contenido del folder
#             folder_content = get_folder_content(folder_path)
            
#             # Enviar la respuesta al cliente
#             client_socket.send(f"Request accepted, stored in buffer #. Scanned by thread #".encode())
#             client_socket.send(folder_content.encode())
#         else:
#             client_socket.send("Request not accepted".encode())
#     else:
#         client_socket.send("Invalid request".encode())
    
#     # Cerrar la conexión con el cliente
#     client_socket.close()

# # Crear un socket y escuchar en el puerto especificado
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(("localhost", SERVER_PORT))
# server_socket.listen(5)

# print("Server started. Listening on port", SERVER_PORT, "...")

# # Manejar los clientes en paralelo
# while True:
#     client_socket, address = server_socket.accept()
#     print("New client connected:", address)
    
#     # Crear un hilo para manejar el cliente
#     client_thread = threading.Thread(target=handle_client, args=(client_socket,))
#     client_thread.start()


import socket
import threading
import queue
import os
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Server for folder scanning with buffer and threads.")
parser.add_argument("port", type=int, help="Port number to listen on")
parser.add_argument("buffer_size", type=int, help="Size of the limited buffer")
parser.add_argument("threads", type=int, help="Number of threads to handle clients")
args = parser.parse_args()

# Server configuration
SERVER_PORT = args.port
BUFFER_SIZE = args.buffer_size
MAX_THREADS = args.threads

# Crear un buffer y un semáforo para controlar el acceso
buffer = queue.Queue(BUFFER_SIZE)
mutex = threading.Lock()
notEmpty = threading.Semaphore(0)
notFull = threading.Semaphore(BUFFER_SIZE)

# Función para obtener el contenido de un folder
def get_folder_content(folder_path):
    try:
        # Obtener el listado de archivos y carpetas en el folder
        contents = os.listdir(folder_path)
        
        # Construir el mensaje con el contenido del folder
        message = "Folder content:\n"
        for item in contents:
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                message += f"[DIR] {item}\n"
            else:
                message += f"[FILE] {item}\n"
        
        return message
    
    except OSError as e:
        # Manejar errores al acceder al folder
        return f"Error accessing folder: {e}"

# Función para manejar los clientes
def handle_client(client_socket):
    # Recibir el mensaje del cliente
    message = client_socket.recv(1024).decode()
    
    # Procesar el mensaje
    if message.startswith("LIST"):
        folder_path = message.split()[1]
        
        # Verificar si hay espacio en el buffer
        if notFull._value > 0:
            # Agregar el mensaje al buffer
            buffer.put(message)
            notFull._value -= 1
            notEmpty._value += 1
            
            # Obtener el contenido del folder
            folder_content = get_folder_content(folder_path)
            
            # Enviar la respuesta al cliente
            client_socket.send(f"Request accepted, stored in buffer #. Scanned by thread #".encode())
            client_socket.send(folder_content.encode())
        else:
            client_socket.send("Request not accepted".encode())
    else:
        client_socket.send("Invalid request".encode())
    
    # Cerrar la conexión con el cliente
    client_socket.close()

# Crear un socket y escuchar en el puerto especificado
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", SERVER_PORT))
server_socket.listen(5)

print("Server started. Listening on port", SERVER_PORT, "...")

<<<<<<< HEAD
    server = Server(host, port, buffer_size, num_threads)
    server.start()
=======
# Manejar los clientes en paralelo
while True:
    client_socket, address = server_socket.accept()
    print("New client connected:", address)
    
    # Crear un hilo para manejar el cliente
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
>>>>>>> parent of f21acf2 (codigo final)
