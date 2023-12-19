import asyncio as aio
from util import delay


async def A(lock: aio.Lock):
    print("Coroutine A waiting to acquire the lock")
    async with lock:
        print("Coroutine A is in the critical section")
        await delay(2)
    print("Coroutine A released the lock")


async def B(lock: aio.Lock):
    print("Coroutine B waiting to acquire the lock")
    async with lock:
        print("Coroutine B is in the critical section")
        await delay(2)
    print("Coroutine B released the lock")


async def main():
    lock = aio.Lock()
    await aio.gather(A(lock), B(lock))


if __name__ == "__main__":
    aio.run(main())
