import asyncio
import aiohttp
from aiohttp import ClientSession


async def fetch_status(session: ClientSession,
                       url: str) -> int:
    one_sec = aiohttp.ClientTimeout(total=1.5)
    async with session.get(url, timeout=one_sec) as result:
        return result.status


async def main():
    session_timeout = aiohttp.ClientTimeout(total=1, connect=.1)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        await fetch_status(session, 'http://localhost:5052/delay')


asyncio.run(main())
