import asyncio as aio, typing as ty, time, queue as q

T = ty.TypeVar('T')
DELAY: float = 2

class Context(ty.Generic[T]):
    def __init__(self, value: T, queue: q.Queue[str] | aio.Queue[str] | None = None) -> None:
        self.value: T = value
        self._q = queue

    def use(self, queue: q.Queue[str] | aio.Queue[str]):
        self._q = queue

    def __enter__(self) -> ty.Self:
        if self._q: self._q.put_nowait("[SYNC] Entered context...")
        time.sleep(DELAY)
        return self

    def __exit__(self, *_) -> None:
        if self._q: self._q.put_nowait("[SYNC] Exited context...")
        time.sleep(DELAY)

    async def __aenter__(self) -> ty.Self:
        if self._q: self._q.put_nowait("[ASYNC] Entered context...")
        return await aio.sleep(DELAY, self)

    async def __aexit__(self, *_) -> None:
        if self._q: self._q.put_nowait("[ASYNC] Exited context...")
        await aio.sleep(DELAY)

def printq(queue: q.Queue[str] | aio.Queue[str]):
    try:
        while item := queue.get_nowait(): print(item)
    except (q.Empty, aio.QueueEmpty): ...

def test_sync_context(ctx: Context[T]) -> T:
    queue = q.Queue()
    ctx.use(queue)
    queue.put("Before sync context")
    with ctx: queue.put(f"In the sync.context: {ctx.value}")
    queue.put("After sync context")
    printq(queue)
    return ctx.value

async def test_async_context(ctx: Context[T]) -> T:
    queue = aio.Queue()
    ctx.use(queue)
    await queue.put("Before async context")
    async with ctx: await queue.put(f"In the async.context: {ctx.value}")
    await queue.put("After async context")
    printq(queue)
    return ctx.value

async def main():
    ctx = Context(5052)
    await test_async_context(ctx)
    print()
    test_sync_context(ctx)

if __name__ == '__main__':
    aio.run(main())