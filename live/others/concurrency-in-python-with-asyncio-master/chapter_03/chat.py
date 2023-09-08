from collections.abc import Iterable
from concurrent.futures import Future, ThreadPoolExecutor, wait
from dataclasses import dataclass, field
import socket
from threading import Lock
from typing import Any, Callable, Optional

# Threaded ChatRoom

class Clients(list[socket.socket]):
    _lock = Lock()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def append(self, __object: socket.socket) -> None:
        with self._lock:
            print(f"New client added: {__object}")
            return super().append(__object)

    def extend(self, __iterable: Iterable[socket.socket]) -> None:
        with self._lock:
            return super().extend(__iterable)

    def send(self, data: bytes):
        torm = []
        with self._lock:
            print(f"Message received: {data.decode()!r}")
            print(f"Sending to {len(self)} people.")
            for client in self:
                try:
                    print(f"Sending to {data!s}: {client}")
                    client.send(data)
                    print("Sent...")
                except Exception as e:
                    print(f"Error communicating with {client}: {str(e)!r}")
                    torm.append(client)
        self.remove(torm)

    def remove(self, clients):
        with self._lock:
            for client in clients:
                super().remove(client)

    def close(self):
        for client in self:
            client.close()
        self.clear()


@dataclass
class ClientWrapper:
    client: socket.socket
    broadcast: Callable[[bytes], Any]

    def __call__(self) -> Any:
        try:
            print("Client Wrapper running")
            while True:
                data = self.client.recv(1024)
                if not data.strip(): continue
                self.broadcast(data)
        except BaseException as e:
            print(f"Client Wrapper error: {str(e)!r}")
        print("Client Wrapper Done")


@dataclass
class ChatRoom:
    host: str
    port: int
    main_task: Optional[Future] = None
    server: socket.socket = field(init=False)
    clients: Clients = field(default_factory=Clients)
    runner: ThreadPoolExecutor = field(default_factory=ThreadPoolExecutor)

    def __post_init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Room Hosted at: {self.host}:{self.port}")

    def _run(self):
        try:
            with self.server, self.clients:
                while True:
                    client, _ = self.server.accept()
                    print(f"New client at {_} added.")
                    self.clients.append(client)
                    wrapped = ClientWrapper(client, self.clients.send)
                    self.runner.submit(wrapped)
        except:
            pass
        finally:
            self.server.close()

    def run(self):
        try:
            self.main_task = self.runner.submit(self._run)
            if self.main_task:
                wait([self.main_task])
        except KeyboardInterrupt:
            if self.main_task:
                self.main_task.cancel()
                self.main_task = None
        self.runner.shutdown(False)


room = ChatRoom("localhost", 9078)
room.run()
