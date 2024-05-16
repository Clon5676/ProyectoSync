import socket
import threading
import os
import sys
import time
from queue import Queue, Full, Empty
import csv
from datetime import datetime

class Server:
    def __init__(self, host, port, buffer_size, num_threads):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.num_threads = num_threads
        self.buffer = Queue(maxsize=buffer_size)
        self.semaphore = threading.Semaphore(0)
        self.lock = threading.Lock()
        self.threads = []
        self.shutdown_event = threading.Event()
        self.output_file = "output.csv"

        with open(self.output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Client IP", "Client Port", "Request", "Thread", "Folder Contents"])

    def start(self):
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f'Server listening on {self.host} port {self.port}')
            try:
                while not self.shutdown_event.is_set():
                    server_socket.settimeout(1.0)
                    try:
                        client_socket, client_address = server_socket.accept()
                        print(f'Connection established with {client_address}')
                        threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()
                    except socket.timeout:
                        continue
            except KeyboardInterrupt:
                print('Server is shutting down...')
                self.shutdown_event.set()
                for _ in range(self.num_threads):
                    self.semaphore.release()
                for thread in self.threads:
                    thread.join()

    def handle_client(self, client_socket, client_address):
        with client_socket:
            client_socket.sendall(f'Communication established with IP {client_address[0]} and port {client_address[1]}'.encode())
            while not self.shutdown_event.is_set():
                try:
                    print(f"Waiting for request from {client_address}")
                    request = client_socket.recv(1024).decode()
                    print(f"Received request: {request}")
                    if not request:
                        break
                    try:
                        self.buffer.put((request, client_address), timeout=1)
                        client_socket.sendall(f'Request accepted and stored in buffer slot {self.buffer.qsize()}'.encode())
                        self.semaphore.release()
                    except Full:
                        client_socket.sendall('Request not accepted, buffer is full. Please retry.'.encode())
                        time.sleep(1)
                except Exception as e:
                    print(f'Error handling client {client_address}: {e}')
                    break

    def worker(self):
        while not self.shutdown_event.is_set():
            self.semaphore.acquire()
            if self.shutdown_event.is_set():
                break
            try:
                request, client_address = self.buffer.get(timeout=1)
                self.process_request(request, client_address)
            except Empty:
                continue

    def process_request(self, request, client_address):
        try:
            print(f"Processing request: {request}")
            folder_content = os.listdir(request)
            response = f'Thread {threading.current_thread().name} processed request. Folder contents: {folder_content}'
            self.buffer.task_done()
            
            with self.lock:
                with open(self.output_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([datetime.now(), client_address[0], client_address[1], request, threading.current_thread().name, folder_content])
        except Exception as e:
            response = f'Error processing request {request}: {e}'
            with self.lock:
                with open(self.output_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([datetime.now(), client_address[0], client_address[1], request, threading.current_thread().name, f"Error: {e}"])
        print(response)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Usage: server.py <host> <port> <buffer_size> <num_threads>')
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    buffer_size = int(sys.argv[3])
    num_threads = int(sys.argv[4])

    server = Server(host, port, buffer_size, num_threads)
    server.start()



""" 
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

# Manejar los clientes en paralelo
while True:
    client_socket, address = server_socket.accept()
    print("New client connected:", address)
    
    # Crear un hilo para manejar el cliente
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start() """