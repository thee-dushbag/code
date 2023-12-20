import asyncio as aio, typing as ty

WorkType = ty.Callable[[], ty.Coroutine[ty.Any, None, None]]


class Worker:
    def __init__(
        self,
        work: WorkType | None = None,
        *,
        restart: bool | None = None,
        delay: float | None = None,
    ):
        self.task: aio.Task | None = None
        self.restart: bool = bool(restart or delay is not None)
        self.delay: float = 0.5 if delay is None else delay
        if work:
            self._worker = work

    @property
    def working(self) -> bool:
        return self.task is None

    def _reset(self, *_):
        self.task = None
        if not self.restart:
            return
        loop = aio.get_running_loop()
        loop.call_later(self.delay, self.start_worker)

    def start_worker(self):
        if self.task:
            return
        self.task = aio.create_task(self._worker())
        self.task.add_done_callback(self._reset)

    def stop_worker(self):
        if not self.task:
            return
        self.task.cancel()

    async def _worker(self):
        """Work to be done Goes HERE"""
        raise NotImplementedError

    def __enter__(self):
        self.start_worker()
        return self

    def __exit__(self, *_):
        self.stop_worker()
