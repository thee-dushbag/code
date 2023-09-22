import asyncio

import aiohttp
from aiohttp import ClientSession
from util import async_timed


@async_timed()
async def fetch_status(session: ClientSession, url: str) -> int:
    async with session.head(url) as result:
        # text = await result.text()
        # print(f"Request Content: {text!r}")
        return result.status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:5052/"
        status = await fetch_status(session, url)
        print(f"Status for {url} was {status}")


asyncio.run(main())
