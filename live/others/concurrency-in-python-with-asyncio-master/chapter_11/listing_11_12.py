import asyncio as aio
from listing_11_11 import FileUpload


class FileServer:
    async def dump_contents_on_complete(self, upload: FileUpload):
        print(await upload.get_contents())

    def onconnect(self, reader: aio.StreamReader, writer: aio.StreamWriter):
        upload = FileUpload(reader, writer)
        upload.listen_for_uploads()
        aio.create_task(self.dump_contents_on_complete(upload))


async def main():
    fileserver = FileServer()
    HOST, PORT = "localhost", 9000
    server = await aio.start_server(fileserver.onconnect, host=HOST, port=PORT)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try: aio.run(main())
    except KeyboardInterrupt: ...
