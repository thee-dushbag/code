import asyncio
from contextvars import ContextVar


class Server:
    address = ContextVar("address")

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def start_server(self):
        server = await asyncio.start_server(self.connected, self.host, self.port)
        await server.serve_forever()

    def connected(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        Server.address.set(writer.get_extra_info("peername"))
        asyncio.create_task(self.recv_msgs(reader))

    async def recv_msgs(self, reader: asyncio.StreamReader):
        while data := await reader.readline():
            print(f"Got message {data.decode()!r} from {Server.address.get()}")


async def main():
    server = Server("127.0.0.1", 9000)
    await server.start_server()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        ...
