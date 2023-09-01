from time import sleep
from typing import Sequence
import asyncio as aio
from mpack.timer import timer

async def grange_async(start, stop, step=1, delay=0.5):
    while start < stop:
        await aio.sleep(delay)
        yield start
        start += step


def grange_sync(start, stop, step=1, delay=0.5):
    while start < stop:
        sleep(delay)
        yield start
        start += step


class With:
    def __init__(self, value: int, delay: float = 0.5) -> None:
        self.value: int = int(value) + 1
        self.delay: float = float(delay)

    def count_sync(self):
        for i in grange_sync(1, self.value, step=1, delay=self.delay):
            print(f"Counting SYNC at: {i}")

    async def count_async(self):
        async for i in grange_async(1, self.value, step=1, delay=self.delay):
            print(f"Counting ASYNC at: {i}")

    async def __aenter__(self):
        print("__AENTER__")
        return self

    async def __aexit__(self, *_):
        print("__AEXIT__")

    def __enter__(self):
        print("__ENTER__")
        return self

    def __exit__(self, *_):
        print("__EXIT__")

@timer
def do_sync_with(value: int, delay: float = .5):
    with With(value, delay) as w:
        w.count_sync()

@timer
async def do_async_with(value: int, delay: float = .5):
    async with With(value, delay) as w:
        await w.count_async()

@timer
async def do_async_with_p(value: int, delay: float = .5):
    async with With(value, delay) as w:
        w.count_sync()

@timer
async def do_async_with_p2(value: int, delay: float = .5):
    with With(value, delay) as w:
        await w.count_async()

@timer
async def do_async_with_n(value: int, delay: float = .5):
    with With(value, delay) as w:
        w.count_sync()

@timer
async def main(argv: Sequence[str]) -> None:
    value: int = 10
    t2 = aio.create_task(do_async_with(value))
    # t1 = aio.create_task(do_async_with_n(value))
    t3 = aio.create_task(do_async_with_p2(value))
    await aio.gather(t2, t3)

if __name__ == "__main__":
    from sys import argv
    aio.run(main(argv[1:]))
