import asyncio

import aiohttp
from util import async_timed

from __init__ import fetch_status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:5052/delay/0"
        fetchers = [
            asyncio.create_task(fetch_status(session, url, 1)),
            asyncio.create_task(fetch_status(session, url, 2)),
            asyncio.create_task(fetch_status(session, url, 3)),
        ]

        done, pending = await asyncio.wait(
            fetchers, return_when=asyncio.FIRST_COMPLETED
        )

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            print(await done_task)


asyncio.run(main())
