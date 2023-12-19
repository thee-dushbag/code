import asyncio as aio


async def acquire(semaphore: aio.Semaphore):
    print("Waiting to acquire")
    async with semaphore:
        print("Acquired")
        await aio.sleep(5)
    print("Releasing")


async def release(semaphore: aio.Semaphore):
    print("Released as a one off!")
    print("Before:", semaphore._value)
    semaphore.release()
    print("After:", semaphore._value)


async def main():
    semaphore = aio.Semaphore(2)
    print("Acquiring twice, releasing three times...")
    await aio.gather(
        acquire(semaphore), acquire(semaphore), release(semaphore), acquire(semaphore)
    )


if __name__ == "__main__":
    aio.run(main())
