import asyncio


async def delay(delay_seconds: int) -> int:
    print(f"sleeping for {delay_seconds} second(s)")
    await asyncio.sleep(delay_seconds)
    print(f"finished sleeping for {delay_seconds} second(s)")
    return delay_seconds


async def wait_for(
    task: asyncio.Task, delay_time: float = 0, *, default=asyncio.CancelledError
):
    time_taken = 0
    while not task.done():
        if time_taken >= delay_time:
            task.cancel()
            break
        time_taken += 0.5
        await asyncio.sleep(0.5)
    try:
        return await task
    except asyncio.CancelledError:
        return default
