import asyncio as aio
from time import sleep
from typing import AsyncGenerator, Generator, Sequence


class OneAtATime:
    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        self.start = start - step
        self.stop = stop - step
        self.step = step

    def __aiter__(self) -> "OneAtATime":
        return self

    def __iter__(self) -> "OneAtATime":
        return self

    def __next__(self) -> int:
        if self.start < self.stop:
            self.start += self.step
        else:
            raise StopIteration
        sleep(1)
        return self.start

    async def __anext__(self) -> int:
        if self.start < self.stop:
            self.start += self.step
        else:
            raise StopAsyncIteration
        await aio.sleep(1)
        return self.start


async def count_to(from_: int, to_: int) -> AsyncGenerator:
    for i in range(from_, to_):
        await aio.sleep(0.5)
        yield i


def count_to_n(from_: int, to_: int) -> Generator:
    for i in range(from_, to_):
        sleep(0.5)
        yield i


async def count_for_n(from_: int, to_: int):
    for i in count_to_n(from_, to_):
        print(f"Count at NORMAL: {i}")


def count_for_ne(from_: int, to_: int):
    for i in count_to_n(from_, to_):
        print(f"Count at NORMAL: {i}")


async def count_for(from_: int, to_: int):
    async for i in count_to(from_, to_):
        print(f"Count at ASYNC_FOR: {i}")


async def one_at_for_n(start: int, stop: int, step: int = 1):
    for i in OneAtATime(start, stop, step):
        print(f"One at a time NORMAL: {i}")


def one_at_for_ne(start: int, stop: int, step: int = 1):
    for i in OneAtATime(start, stop, step):
        print(f"One at a time NORMAL: {i}")


async def one_at_for(start: int, stop: int, step: int = 1):
    async for i in OneAtATime(start, stop, step):
        print(f"One at a time ASYNC_FOR: {i}")


async def main(argv: Sequence[str]) -> None:
    print("\n\t\tNORMAL FOR LOOPS")
    await aio.gather(count_for_n(1, 11), one_at_for_n(1, 15))
    print("\n\t\tNORMAL FOR LOOPS IN EXECUTOR")
    loop = aio.get_running_loop()
    t1 = loop.run_in_executor(None, count_for_ne, 1, 11)
    t2 = loop.run_in_executor(None, one_at_for_ne, 1, 15)
    await aio.gather(t1, t2)
    print("\n\t\tASYNC FOR LOOPS")
    await aio.gather(count_for(1, 11), one_at_for(1, 15))


if __name__ == "__main__":
    from sys import argv

    aio.run(main(argv[1:]))
