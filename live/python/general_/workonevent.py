import asyncio as aio, typing as ty
from mpack.worker import Worker

Param = ty.ParamSpec("Param")
Work = ty.Callable[Param, ty.Coroutine[ty.Any, None, None]]


def count(start: int = 0, step: int = 1) -> ty.Generator[int, None, ty.NoReturn]:
    while True:
        yield start
        start += step


def event_action(workobj: Work[Param], /):
    def get_params(*args: Param.args, **kwargs: Param.kwargs):
        return Worker(lambda: workobj(*args, **kwargs))

    return get_params


@event_action
async def producer(event: aio.Event, delay: float = 1):
    for prod in count(1):
        await aio.sleep(delay)
        print(f"[producer]: Producing {prod}")
        event.set()


@event_action
async def consumer(event: aio.Event, delay: float = 1):
    for prod in count(1):
        await event.wait()
        event.clear()
        print(f"[consumer]: consuming {prod}")
        await aio.sleep(delay)


async def main():
    event = aio.Event()
    with consumer(event, 2), producer(event):
        await aio.sleep(6)


if __name__ == "__main__":
    # Shutdown gracefully.
    try:
        aio.run(main())
    except KeyboardInterrupt:
        ...
