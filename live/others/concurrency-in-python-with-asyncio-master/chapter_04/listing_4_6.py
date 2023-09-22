import asyncio

import aiohttp
from util import async_timed

from __init__ import fetch_status


@async_timed()
async def main():
    tcp_conn = aiohttp.TCPConnector(limit=1000)
    async with aiohttp.ClientSession(connector=tcp_conn) as session:
        requests = [fetch_status(session, "http://localhost:5052") for _ in range(1000)]
        status_codes = await asyncio.gather(*requests)
        print(status_codes)


asyncio.run(main())
