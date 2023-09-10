import asyncio
import aiohttp
import logging
from util import async_timed
from __init__ import fetch_status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        good_request = fetch_status(session, 'http://localhost:5052')
        bad_request = fetch_status(session, 'http://localhost:9080')

        fetchers = [asyncio.create_task(good_request),
                    asyncio.create_task(bad_request)]

        done, pending = await asyncio.wait(fetchers)

        print(f'Done task count: {len(done)}')
        print(f'Pending task count: {len(pending)}')

        for done_task in done:
            # result = await done_task will throw an exception
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error("Request got an exception") #,
                            #   exc_info=done_task.exception())


asyncio.run(main())
