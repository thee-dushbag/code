import asyncio
import logging
from asyncio import StreamReader, StreamWriter


class ServerState:
    def __init__(self):
        self._writers = []

    async def add_client(self, reader: StreamReader, writer: StreamWriter):  # A
        self._writers.append(writer)
        await self._on_connect(writer)
        asyncio.create_task(self._echo(reader, writer))

    async def _on_connect(self, writer: StreamWriter):  # B
        writer.write(f"Welcome! {len(self._writers)} user(s) are online!\n".encode())
        await writer.drain()
        await self._notify_all("New user connected!\n")

    async def _echo(self, reader: StreamReader, writer: StreamWriter):  # C
        try:
            while data := await reader.readline():
                if not data:
                    break
                writer.write(data)
                await writer.drain()
            self._writers.remove(writer)
            writer.close()
            await writer.wait_closed()
            await self._notify_all(
                f"Client disconnected. {len(self._writers)} user(s) are online!\n"
            )
        except Exception as e:
            logging.exception("Error reading from client.", exc_info=e)
            self._writers.remove(writer)
            writer.close()
            await writer.wait_closed()
    
    async def _notify_all(self, message: str):  # D
        for writer in self._writers:
            writer.write(message.encode())
            await writer.drain()

    async def close(self):
        def _close(w):
            w.close()
            return w.wait_closed()

        toclose = (_close(w) for w in self._writers)
        await asyncio.gather(*toclose)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        await self.close()


async def main():
    async with ServerState() as echoserver:
        async with await asyncio.start_server(
            echoserver.add_client, "localhost", 8000
        ) as server:
            await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        ...
