import socket
import threading
import queue

# Constantes
BUFFER_SIZE = 4  # Tamaño del buffer
MAX_THREADS = 2  # Número máximo de hilos que pueden operar en paralelo

# Crear un buffer y un semáforo para controlar el acceso
buffer = queue.Queue(BUFFER_SIZE)
mutex = threading.Lock()
notEmpty = threading.Semaphore(0)
notFull = threading.Semaphore(BUFFER_SIZE)

# Función para manejar los clientes
def handle_client(client_socket):
    # Recibir el mensaje del cliente
    message = client_socket.recv(1024).decode()

    # Procesar el mensaje
    if message.startswith("LIST"):
        # Verificar si hay espacio en el buffer
        if notFull.value > 0:
            # Agregar el mensaje al buffer
            buffer.put(message)
            notFull.value -= 1
            notEmpty.value += 1
            client_socket.send("Request accepted, stored in buffer #".encode())
        else:
            client_socket.send("Request not accepted".encode())
    else:
        client_socket.send("Invalid request".encode())

    # Cerrar la conexión con el cliente
    client_socket.close()

# Crear un socket y escuchar en el puerto especificado
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8087))
server_socket.listen(5)

print("Server started. Listening on port 8087...")

# Manejar los clientes en paralelo
while True:
    client_socket, address = server_socket.accept()
    print("New client connected:", address)

    # Crear un hilo para manejar el cliente
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()