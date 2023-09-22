import asyncio
import logging

import aiohttp
from util import async_timed

from __init__ import fetch_status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, "python://bad.com")),
            asyncio.create_task(
                fetch_status(session, "http://localhost:5052", delay=3)
            ),
            asyncio.create_task(
                fetch_status(session, "http://localhost:5052", delay=3)
            ),
        ]

        done, pending = await asyncio.wait(
            fetchers, return_when=asyncio.FIRST_EXCEPTION
        )

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error(
                    "Request got an exception"  # , exc_info=done_task.exception()
                )

        for pending_task in pending:
            pending_task.cancel()


asyncio.run(main())
