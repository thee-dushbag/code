import asyncio
import logging
from asyncio import StreamReader, StreamWriter


class ChatServer:
    def __init__(self):
        self._username_to_writer: dict[str, asyncio.StreamWriter] = {}
        self._closed = False
        self._chats: list[asyncio.Task] = []

    async def start(self):
        self._closed = False

    async def client_connected(self, reader: StreamReader, writer: StreamWriter):  # A
        try:
            command = await asyncio.wait_for(reader.readline(), 10)
            command, _, args = command.partition(b" ")
            args = args.strip()
            username = args.decode()
            if username in self._username_to_writer:
                writer.write(f"[SERVER]: Username {username} already taken.\n".encode())
            elif command.lower() == b"connect":
                self._add_user(username, reader, writer)
                await self.onconnect(username, writer)
                return
            else:
                writer.write(f"Unknown command {command!s}, available 'connect <username>'\n".encode())
                # logging.error(f"Got invalid command from client, disconnecting. {command}")
        except TimeoutError:
            writer.write(b"You took too long to identify yourself.")
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    def _add_user(self, username: str, reader: StreamReader, writer: StreamWriter):  # B
        self._username_to_writer[username] = writer
        task = asyncio.create_task(self.userchat(username, reader))
        self._chats.append(task)

    async def onconnect(self, username: str, writer: StreamWriter):  # C
        writer.write(
            f"Welcome! {len(self._username_to_writer)} user(s) are online!\n".encode()
        )
        await writer.drain()
        await self.broadcast(f"{username} connected!\n")

    async def _remove_user(self, username: str):
        writer = self._username_to_writer[username]
        writer.close()
        await writer.wait_closed()
        del self._username_to_writer[username]

    async def userchat(self, username: str, reader: StreamReader):  # D
        try:
            while (data := await asyncio.wait_for(reader.readline(), 20)) != b"":
                await self.broadcast(f"{username}: {data.decode()}")
        except asyncio.TimeoutError:
            await self.broadcast(f"[SERVER]: {username} idling around, kicked out.\n")
        finally:
            await self._remove_user(username)
            await self.broadcast(f"[SERVER]: {username} has left the chat\n")

    async def broadcast(self, message: str):  # E
        for writer in self._username_to_writer.values():
            writer.write(message.encode())
            await writer.drain()

    async def close(self):
        await self.broadcast("Server shutting down...\n")
        self._closed = True

        def _close(writer):
            writer.close()
            return writer.wait_closed()

        toclose = (_close(w) for w in self._username_to_writer.values())
        await asyncio.gather(*toclose)
        
        for chat in self._chats:
            chat.cancel()

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, *_):
        if not self._closed:
            await self.close()

    def __del__(self):
        if not self._closed:
            asyncio.create_task(self.close())


async def main():
    async with ChatServer() as chatserver:
        async with await asyncio.start_server(
            chatserver.client_connected, "localhost", 8000
        ) as server:
            await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        ...
