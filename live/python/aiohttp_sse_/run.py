import asyncio as aio
import random as r
import typing as ty
from itertools import count

import mpack.bqueue as bq

T = ty.TypeVar("T")


async def processor(
    q: bq.bQueue[T],
    process: ty.Callable[[T], ty.Coroutine[None, None, ty.Any]],
):
    print("Processor Starting Up...")
    async with aio.TaskGroup() as runner:
        waiter = None
        try:
            for i in count(1):
                print(q)
                waiter = q.pop()
                item = await waiter
                print(q)
                print(f"Processing item[{i}]: {item!r}")
                runner.create_task(process(item))
        except aio.CancelledError:
            # await q.push(ty.cast(T, None))
            q.release_waiter(waiter)  # type:ignore
        except bq.NoValue:
            ...
    print(q)
    print("Processor Shutting Down...")


async def process(x: int) -> int:
    print(f"Computing sqr({x})")
    await aio.sleep(3)
    print(f"Computed sqr({x})= {x ** 2}")
    return x**2


async def main():
    q = bq.bQueue(3)
    task = aio.create_task(processor(q, process))
    await aio.gather(*(q.push(r.randint(100, 1000)) for _ in range(7)))
    task.cancel("bq going away")
    print(q)
    await task
    print(q)
    print(q._waiters.pop().done())


aio.run(main())
