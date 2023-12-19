import asyncio as aio


async def do_work(condition: aio.Condition, wid: int):
    while True:
        print(f"{wid}: Waiting for condition lock...")
        async with condition:
            print(f"{wid}: Acquired lock, releasing and waiting for condition...")
            await condition.wait()
            print(f"{wid}: Condition event fired, re-acquiring lock and doing work...")
            await aio.sleep(1)
        print(f"{wid}: Work finished, lock released.")


async def fire_event(condition: aio.Condition):
    while True:
        await aio.sleep(3)
        print("About to notify, acquiring condition lock...")
        async with condition:
            print("Lock acquired, notifying all workers.")
            condition.notify_all()
        print("Notification finished, releasing lock.")


async def main():
    condition = aio.Condition()

    aio.create_task(fire_event(condition))
    await aio.gather(do_work(condition, 1), do_work(condition, 2))


if __name__ == "__main__":
    try: aio.run(main())
    except KeyboardInterrupt: ...
