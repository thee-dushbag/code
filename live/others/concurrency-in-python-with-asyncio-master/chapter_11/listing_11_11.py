import asyncio as aio


class FileUpload:
    def __init__(self, reader: aio.StreamReader, writer: aio.StreamWriter):
        self._reader = reader
        self._writer = writer
        self._finished_event = aio.Event()
        self._buffer = b""
        self._upload_task = None

    def listen_for_uploads(self):
        self._upload_task = aio.create_task(self._accept_upload())

    async def _accept_upload(self):
        while data := await self._reader.read(1024):
            self._buffer += data
        self._finished_event.set()
        self._writer.close()
        await self._writer.wait_closed()

    async def get_contents(self):
        await self._finished_event.wait()
        return self._buffer
