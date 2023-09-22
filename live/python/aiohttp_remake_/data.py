import asyncio as aio
from typing import Sequence

from httpx import AsyncClient
from yarl import URL

HOST, PORT = "localhost", 5052
BASE_URL = URL(f"http://{HOST}:{PORT}")
NOTE_URL = BASE_URL.with_path("notes")


async def main(argv: Sequence[str]) -> None:
    async with AsyncClient(base_url=str(BASE_URL)) as client:
        ...


if __name__ == "__main__":
    from sys import argv

    aio.run(main(argv[1:]))
