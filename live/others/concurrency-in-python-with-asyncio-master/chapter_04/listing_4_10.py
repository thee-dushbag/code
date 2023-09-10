import asyncio
import aiohttp
from util import async_timed
from __init__ import fetch_status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = \
          [asyncio.create_task(fetch_status(session, 'http://localhost:5052')),
           asyncio.create_task(fetch_status(session, 'http://localhost:5052'))]
        done, pending = await asyncio.wait(fetchers)

        print(f'Done task count: {len(done)}')
        print(f'Pending task count: {len(pending)}')

        for done_task in done:
            result = await done_task
            print(result)


asyncio.run(main())
