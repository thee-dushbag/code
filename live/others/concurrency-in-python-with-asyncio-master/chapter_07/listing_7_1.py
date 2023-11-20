from collections.abc import Callable, Iterable, Mapping
import socket
from threading import Thread

def echo(client: socket.socket):
    while True:
        data = client.recv(2048)
        if not data: return
        print(f"[{client.getpeername()[1]}] Received {data}, sending!")
        client.sendall(data)

class EchoThread(Thread):
    def __init__(self, connection: socket.socket, *, daemon=None) -> None:
        super().__init__(None, None, None, (), None, daemon=daemon)
        self.conn = connection
        self.connid = connection.getpeername()[1]

    def __enter__(self):
        print(f"New Connection from: {self.connid}")
        return self
    
    def __exit__(self, *_, **__):
        print(f"Connection closed: {self.connid}")

    def run(self):
        with self:
            while True:
                data = self.conn.recv(2048)
                if not data: return
                print(f"[{self.connid}] Received {data}, sending!")
                self.conn.sendall(data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 8000))
    server.listen()
    while True:
        connection, _ = server.accept()  # A
        EchoThread(connection, daemon=True).start()
