import asyncio as aio


def trigger_event(event: aio.Event):
    print("Triggering event!")
    event.set()


async def do_work_on_event(event: aio.Event):
    print("Waiting for event...")
    await event.wait()
    print("Performing work!")
    await aio.sleep(0.5)
    print("Finished work!")
    event.clear()


async def main():
    event = aio.Event()
    aio.get_running_loop().call_later(3.0, trigger_event, event)
    aio.get_running_loop().call_later(6.0, trigger_event, event)
    await aio.gather(do_work_on_event(event), do_work_on_event(event))
    await do_work_on_event(event)


if __name__ == "__main__":
    aio.run(main())
