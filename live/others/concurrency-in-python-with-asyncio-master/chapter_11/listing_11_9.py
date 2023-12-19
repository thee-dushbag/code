import asyncio as aio


async def main():
    bounded_semaphore = aio.BoundedSemaphore(1)

    await bounded_semaphore.acquire()
    bounded_semaphore.release()
    bounded_semaphore.release()


if __name__ == "__main__":
    aio.run(main())
