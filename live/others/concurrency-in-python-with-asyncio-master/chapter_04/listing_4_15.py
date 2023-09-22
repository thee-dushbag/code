import asyncio

import aiohttp
from util import async_timed

from __init__ import fetch_status, url

url = url + "/delay/0"


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url, delay=3)),
        ]

        done, pending = await asyncio.wait(fetchers, timeout=1)

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            result = await done_task
            print(result)


asyncio.run(main())
