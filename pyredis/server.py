import socket

from pyredis.commands import handle_command
from pyredis.protocol import encode_message, extract_frame_from_buffer

RECV_SIZE = 2048

class Server:
    def __init__(self, port):
        self.port = port
        self._running = False

    def run(self):
        self._running = True

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            self._server_socket = server_socket
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind to an address and listen for incoming connections.
            server_socket.bind("127.0.0.1")
            server_socket.listen()

            while self._running:
                conn, _ = server_socket.accept()
                handle_client_connection(conn)
                

    def stop(self):
        self._running = False

def handle_client_connection(
    connection:socket.socket
):
    buffer = bytearray()

    try:
        while True:
            data = connection.recv(RECV_SIZE)

            if not data:
                break

            buffer.extend(data)

    finally:
        connection.close()