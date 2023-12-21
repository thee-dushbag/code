import asyncio as aio


async def _echo(broadcast, reader: aio.StreamReader, writer: aio.StreamWriter):
    while line := await reader.readline():
        await broadcast(writer, line)


class Chat:
    def __init__(self) -> None:
        self.clients: list[aio.StreamWriter] = []
        self.closed = False

    async def remove_client(self, client: aio.StreamWriter):
        self.clients.remove(client)
        client.close()
        await self.broadcast(
            client, f"Client disconnected, {len(self.clients)}\n".encode()
        )
        await client.wait_closed()

    async def broadcast(self, sender: aio.StreamWriter | None, msg: bytes):
        def sendmsg(client: aio.StreamWriter):
            if client is not sender:
                client.write(msg)
            return client.drain()

        sendtasks = (sendmsg(c) for c in self.clients)
        await aio.gather(*sendtasks)

    async def chat(self, reader: aio.StreamReader, writer: aio.StreamWriter):
        task = aio.create_task(_echo(self.broadcast, reader, writer))
        disconnect_cb = lambda _: aio.create_task(self.remove_client(writer))
        task.add_done_callback(disconnect_cb)
        self.clients.append(writer)
        await self.broadcast(
            writer, f"Client connected, {len(self.clients)} clients.\n".encode()
        )

    async def close(self):
        self.closed = True
        if not self.clients: return
        await self.broadcast(None, b"Server shutting down....\n")
        def closenwait(c: aio.StreamWriter):
            c.close()
            return c.wait_closed()
        await aio.gather(*(closenwait(c) for c in self.clients))

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        await self.close()

    def __del__(self):
        if not self.closed:
            aio.create_task(self.close())


class _GeneratorContext:
    def __init__(self, generator) -> None:
        self._generator = generator
        self._ctx = None

    def __call__(self, *args, **kwargs):
        self._ctx = self._generator(*args, **kwargs)
        return self

    def __enter__(self):
        if self._ctx is None:
            raise RuntimeError("_GeneratorContext was not initialized.")
        return next(self._ctx)

    def __exit__(self, etype: type[BaseException], eval: BaseException, etraceb):
        if self._ctx:
            try:
                anext(self._ctx)
            except StopIteration:
                ...
            else:
                raise ValueError(
                    "Passed generator yielded more than once"
                ) from eval


@_GeneratorContext
def PathContext(path: str):
    try:
        yield path
    finally:
        import os

        if os.path.exists(path):
            os.unlink(path)


async def main():
    with PathContext("./echo_server") as path:
        async with Chat() as chatserver:
            async with await aio.start_unix_server(chatserver.chat, path) as server:
                await server.serve_forever()


if __name__ == "__main__":
    try:
        aio.run(main())
    except KeyboardInterrupt:
        ...
