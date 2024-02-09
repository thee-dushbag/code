import asyncio as aio
from pathlib import Path


def _islower(byte: int) -> bool:
    return 97 <= byte <= 122


def _isupper(byte: int) -> bool:
    return 65 <= byte <= 90


def _toggle(byte: int) -> int:
    return byte + (_islower(byte) * -1 + _isupper(byte)) * 32


async def echo(reader: aio.StreamReader, writer: aio.StreamWriter):
    try:
        while chunk := await reader.read(1024):
            toggled = bytes(_toggle(b) for b in chunk)
            writer.write(toggled)
            await writer.drain()
    except aio.CancelledError:
        ...
    finally:
        writer.close()
        await writer.wait_closed()


async def serve(file: Path):
    server = await aio.start_unix_server(echo, file)
    async with server:
        await server.serve_forever()


async def main():
    file = Path.cwd() / "socket"
    if file.exists():
        raise FileExistsError(file)
    try:
        await serve(file)
    finally:
        file.unlink(True)


if __name__ == "__main__":
    try:
        aio.run(main())
    except KeyboardInterrupt:
        ...
