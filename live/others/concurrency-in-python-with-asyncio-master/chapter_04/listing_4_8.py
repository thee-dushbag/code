import asyncio

import aiohttp
from util import async_timed

from __init__ import fetch_status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, "http://localhost:5052", 1),
            fetch_status(session, "http://localhost:5052", 1),
            fetch_status(session, "http://localhost:5052", 10),
        ]

        for finished_task in asyncio.as_completed(fetchers):
            print(await finished_task)


asyncio.run(main())
