import contextlib
import functools
from typing import (
    Callable,
    ParamSpec,
    Sequence,
    TypeVar,
    TypeVarTuple,
    TypedDict,
    Unpack,
)
from time import monotonic, sleep
from threading import Event, Thread
from mpack import retry

P = ParamSpec("P")
T = TypeVar("T")
Ts = TypeVarTuple("Ts")


def mprint(*values: Unpack[Ts]):
    for value in values:
        print(value, end=" ")
    print()


def timer(func: Callable[P, T]) -> Callable[P, T]:
    @functools.wraps(func)
    def timeit(*args: P.args, **kwargs: P.kwargs) -> T:
        start = monotonic()
        result: T = func(*args, **kwargs)
        lapse = monotonic() - start
        print("%s took %.4f seconds" % (func.__name__, lapse))
        return result

    return timeit


@timer
def count(stop: int, delay: float | None = None):
    delay = 0.1 if delay is None else delay
    for _ in range(stop):
        sleep(delay)


from os_local import setos, getos


def throw_times(
    count: int,
    error: type[Exception] = Exception,
    *,
    catch: Sequence[type[Exception]] | None = None,
    retries: int | None = None,
    wait: float | None = None,
):
    @retry.retry(count=retries, on=catch, delay=wait)
    def thrower(result: T) -> T:
        nonlocal count
        while count:
            print("Count: %s" % count)
            count -= 1
            raise error("Count at %s" % count)
        return result

    return thrower


def show_os(name: str, wait_event: Event):
    print(f"1. Thread {name} can see os={getos()}")
    wait_event.wait()
    print(f"2. Thread {name} can see os={getos()}")


class ShowOSKwargs(TypedDict):
    name: str
    wait_event: Event


def main():
    thrower = throw_times(5, KeyError, retries=6, wait=1)
    with contextlib.suppress(retry.RetryError):
        result = thrower("Hello World")
        print("Result: %r" % result)
    event = Event()
    infos: list[ShowOSKwargs] = [
        {"name": "One", "wait_event": event},
        {"name": "Two", "wait_event": event},
    ]
    threads = [Thread(target=show_os, kwargs=info) for info in infos]
    for thread in threads:
        thread.start()
    setos("windows")
    event.set()
    for thread in threads:
        thread.join()
    # Must be run after setting event to prevent deadlock
    # Since the main thread is also the event setter.
    show_os("main", event)


if __name__ == "__main__":
    main()
