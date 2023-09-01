import asyncio as aio
from typing import Any, Sequence
from time import sleep
import mpack.timer as _t


class OneAtATime:
    def __init__(self, start: int, stop: int, step: int = 1, delay: float = 1):
        self.start = start - step
        self.step = step
        self.delay = delay
        self.stop = stop - step

    def _iter(self):
        sleep(self.delay)
        return self

    def __iter__(self):
        return self._iter()

    def __aiter__(self):
        return self._iter()

    def _next(self, err) -> int:
        if self.start >= self.stop:
            raise err
        self.start += self.step
        return self.start

    async def __anext__(self):
        await aio.sleep(self.delay)
        return self._next(StopAsyncIteration)

    def __next__(self):
        sleep(self.delay)
        return self._next(StopIteration)


async def oneatatime_for_normal(start: int, stop: int, delay: float = 0.5):
    for i in OneAtATime(start, stop, delay=delay):
        print(f"[NORMAL FOR LOOP]: i: {i}")


async def oneatatime_for(start: int, stop: int, delay: float = 0.5):
    async for i in OneAtATime(start, stop, delay=delay):
        print(f"[ASYNC FOR LOOP]: i: {i}")


async def test_oneatatime_for_func(
    func, starts: tuple[int, int], stops: tuple[int, int], delay: float = 0.5
):
    t1 = func(starts[0], stops[0], delay)
    t2 = func(starts[1], stops[1], delay)
    await aio.gather(t1, t2)


@_t.timer
async def test_oneatatime_for(
    starts: tuple[int, int], stops: tuple[int, int], delay: float = 0.5
):
    await test_oneatatime_for_func(oneatatime_for, starts, stops, delay)


@_t.timer
async def test_oneatatime_for_normal(
    starts: tuple[int, int], stops: tuple[int, int], delay: float = 0.5
):
    await test_oneatatime_for_func(oneatatime_for_normal, starts, stops, delay)


@_t.timer
async def gather(
    *tasks: aio.Task | aio.Future, return_exceptions: bool = True
) -> list[Any]:
    return await aio.gather(*tasks, return_exceptions=return_exceptions)


async def main(argv: Sequence[str]) -> None:
    starts, stops, delay = (1, 1), (11, 6), 1
    r1 = await test_oneatatime_for(starts, stops, delay)
    r2 = await test_oneatatime_for_normal(starts, stops, delay)
    print(r1, r2, sep="\n")
    t1 = test_oneatatime_for(starts, stops, delay)
    t2 = test_oneatatime_for_normal(starts, stops, delay)
    gtime = await gather(t2, t1)
    r1, r2 = gtime.result
    print(r1, r2, gtime, sep="\n")


if __name__ == "__main__":
    from sys import argv

    aio.run(main(argv[1:]))
