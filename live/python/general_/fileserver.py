import asyncio as aio, typing as ty


class SizeB:
    def __init__(self, unit: int | None = None, /) -> None:
        self._unit = 1024 if unit is None else unit

    @property
    def bytes(self) -> int:
        return 8

    @property
    def unit(self) -> int:
        return self._unit

    @property
    def kilo_bytes(self) -> int:
        return self.bytes * self.unit
        # return 8 * self.unit

    @property
    def mega_bytes(self) -> int:
        return self.kilo_bytes * self.unit
        # return 8 * self.unit**2

    @property
    def giga_bytes(self) -> int:
        return self.mega_bytes * self.unit
        # return 8 * self.unit**3

    @property
    def tera_bytes(self) -> int:
        return self.giga_bytes * self.unit
        # return 8 * self.unit**4

    @property
    def peta_bytes(self) -> int:
        return self.tera_bytes * self.unit
        # return 8 * self.unit**5

    b = bytes
    kb = kilo_bytes
    mb = mega_bytes
    gb = giga_bytes
    tb = tera_bytes
    pb = peta_bytes


class Upload:
    def __init__(
        self, source: aio.StreamReader, /, *, chunk_size: int | None = None
    ) -> None:
        self._source = source
        self._done = aio.Event()
        self._contents = b""
        aio.create_task(self._downloader(chunk_size or SizeB().kb * 64))

    async def _downloader(self, chunk_size: int):
        while chunk := await self._source.read(chunk_size):
            self._contents += chunk
        self._done.set()

    async def contents(self) -> bytes:
        await self._done.wait()
        return self._contents


async def FileServer(reader: aio.StreamReader, writer: aio.StreamWriter):
    contents = await Upload(reader).contents()
    print(contents)
    writer.close()
    await writer.wait_closed()


async def main():
    server = await aio.start_unix_server(FileServer, "/home/simon/Desktop/server")
    async with server: await server.serve_forever()


if __name__ == "__main__":
    try:
        aio.run(main())
    except KeyboardInterrupt:
        ...
