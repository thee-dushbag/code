import asyncio as aio
import typing as ty
from functools import wraps

import janus
from attrs import define, field


def make_async(func):
    @wraps(func)
    async def _async_func(*args, **kwargs):
        return func(*args, **kwargs)

    return _async_func


def on_line_no_line(func):
    @wraps(func)
    async def _on_line(line, Line):
        return await func(line)

    return _on_line


def on_error_no_line(func):
    @wraps(func)
    async def _on_error(line, exc, Line):
        return await func(line, exc)

    return _on_error


aprint = on_line_no_line(make_async(print))

T = ty.TypeVar("T")
K = ty.TypeVar("K")
SpecialLineCallback = ty.Callable[
    ["Line[T, K]", "SpecialLine[K, ty.Any]"], ty.Coroutine[None, None, ty.Any]
]
OnLineCallback = ty.Callable[[T, "Line"], ty.Coroutine[None, None, ty.Any]]
OnErrorCallback = ty.Callable[
    [T, "Exception", "Line"], ty.Coroutine[None, None, ty.Any]
]


class LineError(Exception):
    ...


class StopRunner(LineError, aio.CancelledError):
    ...


@define
class SpecialLine(ty.Generic[K, T]):
    key: K
    value: T | None = None


class SpecialLineCallbackMap(dict[K, SpecialLineCallback]):
    ...


async def _consume_line(line: ty.Any, special_line: ty.Any):
    ...


async def _stop_runner(line: "Line", special):
    await line._force_stop()


async def _force_stop_runner(line: "Line", special):
    raise StopRunner


def default_special_line():
    return SpecialLineCallbackMap(stop=_stop_runner, force_stop=_force_stop_runner)


@define()
class Line(ty.Generic[T, K]):
    _on_line_callback: OnLineCallback = field(default=aprint)
    _on_error_callback: OnErrorCallback = field(default=aprint)
    _line_cache: janus.Queue[T | SpecialLine[K, ty.Any]] = field(
        init=False, factory=janus.Queue
    )
    _special_lines_map: SpecialLineCallbackMap[K] = field(factory=default_special_line)
    _runner_task: aio.Task | None = None
    timeout: float | None = field(default=None)

    async def __aenter__(self):
        self._start_runner()
        return self

    async def __aexit__(self, *_, **__):
        await self._stop_runner(self.timeout)

    def special(self, key: K):
        def _callback(func: SpecialLineCallback):
            self._special_lines_map[key] = func
            return func

        return _callback

    async def _wait_stop(self, timeout: float | None = None):
        if self._runner_task is None:
            return
        if timeout is None:
            timeout = self.timeout
        await aio.wait_for(self._runner_task, timeout)

    def _start_runner(self):
        if self._runner_task is None:
            self._runner_task = aio.create_task(self._runner())

    async def _force_stop(self):
        if self._runner_task is not None:
            self._line_cache = janus.Queue()
            self._runner_task.cancel()
            self._runner_task = None

    async def _stop_runner(self, timeout: float | None = None):
        line = SpecialLine(ty.cast(K, "stop"), None)
        await self._async_add_line(line)
        await self._wait_stop(timeout)

    async def on_line(self, line: T):
        await self._on_line_callback(line, self)

    async def on_error(self, line: T, error: Exception):
        await self._on_error_callback(line, error, self)

    async def add_async_line(self, line: T | SpecialLine[K, ty.Any]):
        await self._async_add_line(line)

    def add_line(self, line: T | SpecialLine[K, ty.Any]):
        self._sync_add_line(line)

    async def _async_add_line(self, line: T | SpecialLine[K, ty.Any]):
        await self._line_cache.async_q.put(line)

    def _sync_add_line(self, line: T | SpecialLine[K, ty.Any]):
        self._line_cache.sync_q.put(line)

    async def _dispatch_special(self, line: SpecialLine[K, ty.Any]):
        callback = self._special_lines_map.get(line.key, _consume_line)
        await callback(self, line)  # type: ignore

    async def _line(self, line: T):
        try:
            await self.on_line(line)
        except Exception as e:
            await self.on_error(line, e)

    async def _dispatch_line(self, line: T | SpecialLine[K, ty.Any]):
        if isinstance(line, SpecialLine):
            return await self._dispatch_special(line)
        await self._line(line)

    async def _run(self):
        async with aio.TaskGroup() as task:
            while line := await self._line_cache.async_q.get():
                task.create_task(self._dispatch_line(line))

    async def _runner(self):
        try:
            await aio.create_task(self._run())
        except (StopRunner, aio.CancelledError) as e:
            ...
