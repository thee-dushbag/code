import asyncio as aio
from time import sleep
from typing import Sequence


async def echo(reader: aio.StreamReader, writer: aio.StreamWriter):
    print("New Connection.")
    try:
        while data := await reader.readline():
            print(f"Received: {data}")
            writer.write(data.upper())
            await writer.drain()
        print("Leaving Connection.")
    except aio.CancelledError as err:
        print("Connection dropped! Cleaning up.")
        for i in range(1, 11):
            print(f"Wait at: {i}")
            sleep(0.5)
        print("Done cleaning. Free sockets.")


async def start_server(host: str = "localhost", port: int = 8888) -> None:
    async with (server := await aio.start_server(echo, host=host, port=port)):
        await server.serve_forever()


async def main(argv: Sequence[str]) -> None:
    host, port = "localhost", 8888
    if len(argv) > 2:
        host, port = argv[0], int(argv[1])
    await start_server(host, port)


if __name__ == "__main__":
    from sys import argv

    try:
        aio.run(main(argv[1:]))
    except KeyboardInterrupt as k:
        print("Done.")
