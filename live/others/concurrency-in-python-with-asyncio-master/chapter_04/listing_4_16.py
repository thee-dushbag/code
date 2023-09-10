import asyncio
import aiohttp
from __init__ import fetch_status, url

url += '/delay/0'

async def main():
    async with aiohttp.ClientSession() as session:
        totask = asyncio.create_task
        api_a = totask(fetch_status(session, url))
        api_b = totask(fetch_status(session, url, delay=2))

        done, pending = await asyncio.wait([api_a, api_b], timeout=1)

        for task in pending:
            if task is api_b:
                print("API B too slow, cancelling")
                task.cancel()


asyncio.run(main())
