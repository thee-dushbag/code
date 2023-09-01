import typing, threading, asyncio
from typing import Any

T = typing.TypeVar("T")
_QBASESIZE = -1


class _Sentinel:
    ...


_MISSING = _Sentinel()


class _Pusher(typing.Generic[T]):
    def __init__(self, value: T, future: asyncio.Future[None]) -> None:
        self._future = future
        self._value = value

    def get_value(self) -> T:
        self._future.set_result(None)
        return self._value

    def __str__(self):
        return f"<Pusher: {self._value!r}>"


class Waiter(asyncio.Future[T]):
    def __str__(self):
        return f"<Waiter>"

    def set_result(self, __result: T) -> None:
        print(f"Setting Waiter Value: {__result}")
        return super().set_result(__result)

    def cancel(self, msg: Any | None = None) -> bool:
        self.set_exception(NoValue)
        return True


class Pusher(asyncio.Future[T]):
    ...


class QError(Exception):
    ...


class Empty(QError):
    ...


class Full(QError):
    ...


class NoValue(QError):
    ...


class _SimpleQueue(typing.Generic[T]):
    def __init__(self, size: int | None = None) -> None:
        self._values: list[T] = []
        self._size = int(size) if size is not None else _QBASESIZE
        self._qsize: int = 0
        assert self._size >= _QBASESIZE

    def clear(self):
        self._values.clear()
        self._qsize = 0

    def remove(self, value: T):
        self._values = [val for val in self._values if val is value]

    @property
    def size(self) -> int:
        return self._size

    @property
    def qsize(self) -> int:
        return self._qsize

    def empty(self):
        return self._qsize == 0

    def full(self):
        return self._qsize == self._size

    def pop(self) -> T:
        if self.empty():
            raise Empty
        self._qsize -= 1
        return self._values.pop(0)

    def push(self, value: T) -> None:
        if self.full():
            raise Full
        self._qsize += 1
        self._values.append(value)

    def __bool__(self) -> bool:
        return bool(self._values)

    def __str__(self):
        return f"<{', '.join(str(v) for v in self._values)}{': ' if self else ''}{self.qsize}>"


class SimpleQueue(_SimpleQueue[T]):
    def __init__(self, size: int | None = None) -> None:
        super().__init__(size)
        self._lock = threading.Lock()

    def pop(self) -> T:
        with self._lock:
            return super().pop()

    def push(self, value: T) -> None:
        with self._lock:
            return super().push(value)

    def clear(self):
        with self._lock:
            return super().clear()


class bQueue(typing.Generic[T]):
    def __init__(
        self,
        cache_size: int | None = None,
        *,
        waiter_size: int | None = None,
        pusher_size: int | None = None,
    ) -> None:
        self._values: _SimpleQueue[T] = _SimpleQueue(cache_size)
        self._pushers: _SimpleQueue[_Pusher] = _SimpleQueue(pusher_size)
        self._waiters: _SimpleQueue[Waiter] = _SimpleQueue(waiter_size)
        self._lock = threading.Lock()

    def __bool__(self):
        return bool(self._values)

    # def __del__(self):
    #     self.clear()

    def clear(self):
        self._notify_waiters_no_result()
        self._release_pushers()
        self._values.clear()

    def _notify_waiters_no_result(self):
        for waiter in self._waiters._values:
            waiter.set_exception(NoValue)
        self._waiters.clear()

    def _release_pushers(self):
        for pusher in self._pushers._values:
            pusher.get_value()
        self._pushers.clear()

    @property
    def size(self) -> int:
        return self._values._size

    @property
    def qsize(self) -> int:
        return self._values.qsize

    def empty(self) -> bool:
        return self._values.empty()

    def full(self) -> bool:
        return self._values.full()

    def release_waiter(self, waiter: Waiter):
        self._waiters.remove(waiter)
        if not waiter.done():
            waiter.set_exception(NoValue)

    def pop(self) -> Waiter[T]:
        with self._lock:
            prom = asyncio.shield(Waiter())
            if self.empty():
                if self._waiters.full():
                    prom.set_exception(Full)
                else:
                    self._waiters.push(prom)
            else:
                value = self._values.pop()
                prom.set_result(value)
                if self._pushers:
                    pusher = self._pushers.pop()
                    self._values.push(pusher.get_value())
            return prom

    def push(self, value: T) -> Pusher[T]:
        with self._lock:
            prom = asyncio.shield(Pusher())
            if self._waiters:
                waiter = self._waiters.pop()
                waiter.set_result(value)
                prom.set_result(typing.cast(T, None))
            elif self.full():
                if self._pushers.full():
                    prom.set_exception(Full)
                else:
                    pusher = _Pusher(value, prom)
                    self._pushers.push(pusher)
            else:
                self._values.push(value)
                prom.set_result(typing.cast(T, None))
            return prom

    def pop_nowait(self, default=_MISSING):
        with self._lock:
            if self._waiters or self.empty():
                if default is _MISSING:
                    raise NoValue
                return default
            return self._values.pop()

    def push_nowait(self, value: T, default=_MISSING):
        with self._lock:
            if self._pushers or self.full():
                if default is _MISSING:
                    raise Full
            self._values.push(value)

    def __str__(self) -> str:
        return f"bQueue(cache={self._values}, waiters={self._waiters}, pushers={self._pushers})"
