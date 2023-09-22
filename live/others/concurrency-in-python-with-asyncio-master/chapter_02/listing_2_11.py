import asyncio
from asyncio import CancelledError

from util import delay, wait_for


async def close_cleanly(delay_time: int) -> None:
    print("Open Connections...")
    await asyncio.sleep(1)
    try:
        await delay(delay_time)
    except CancelledError:
        print("Cancelled, cleaning up.")
    else:
        print("Task Complete...")
    await asyncio.sleep(1)
    print("Close Connections...")


async def main():
    long_task = asyncio.create_task(close_cleanly(7))
    await wait_for(long_task, 5)


asyncio.run(main())
