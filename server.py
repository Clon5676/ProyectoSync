import socket
import threading
import os
import sys
import time
from queue import Queue, Full, Empty

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
                        self.buffer.put(request, timeout=1)
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
                request = self.buffer.get(timeout=1)
                self.process_request(request)
            except Empty:
                continue

    def process_request(self, request):
        try:
            print(f"Processing request: {request}")
            folder_content = os.listdir(request)
            response = f'Thread {threading.current_thread().name} processed request. Folder contents: {folder_content}'
            self.buffer.task_done()
        except Exception as e:
            response = f'Error processing request {request}: {e}'
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