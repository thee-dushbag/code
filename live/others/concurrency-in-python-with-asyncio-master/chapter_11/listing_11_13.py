import asyncio
from asyncio import Event
from contextlib import suppress


async def trigger_event_periodically(event: Event):
    while True:
        print("Triggering event!")
        event.set()
        await asyncio.sleep(0.2)


async def do_work_on_event(event: Event):
    while True:
        print("Waiting for event...")
        await event.wait()
        event.clear()
        print("Performing work!")
        await asyncio.sleep(2)
        print("Finished work!")


async def main():
    event = asyncio.Event()
    trigger = asyncio.wait_for(trigger_event_periodically(event), 5)

    with suppress(asyncio.TimeoutError):
        await asyncio.gather(do_work_on_event(event), do_work_on_event(event), trigger)


if __name__ == "__main__":
    asyncio.run(main())
