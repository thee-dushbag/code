from mpack.timer import timer_sync  # A timer function
from functools import wraps, lru_cache  # Caching mechanism provided by python std
from sys import (
    setrecursionlimit,
)  # Making sure we don't hit the recursion exceeded limit
from tqdm import (
    tqdm,
)  # A simple progress bar to see how far we've gone in generating the factorials

setrecursionlimit(15000)


# Normal Non-cache function.
def fact(n: int, /) -> int:
    if n <= 1:
        return 1
    return n * fact(n - 1)


# Cached factorial function.
@lru_cache
def cached_fact(n: int, /) -> int:
    if n <= 1:
        return 1
    return n * cached_fact(n - 1)


# Test the time taken to call f multiple times.
def benchmark(f):
    @timer_sync
    @wraps(f)
    def wrapper(r: range):
        # Repeatedly call the function f n times where n = len(r)
        for i in tqdm(r):
            f(i)

    return wrapper


def main(start: int, stop: int, step: int = 1):
    tests = []
    for f in [benchmark(fact), benchmark(cached_fact)]:
        tests.append(f(range(start, stop, step)))
        print(tests[-1])
    tests_sorted = sorted(tests, key=lambda t: t.lapse.time, reverse=True)
    mintime = tests_sorted[-1]
    tests_sorted.reverse()
    for test in tests_sorted:
        print(f"{test.lapse.time/mintime.lapse.time}x: {test}")


def test_facts():
    # Test that all factorial functions return
    # the expected output.
    from math import factorial  # We know this returns the correct answer

    for i in range(100):
        # Get the correct answer
        _actual = factorial(i)
        # Test against the correct answer
        assert _actual == (
            _ := fact(i)
        ), f"Wrong output for fact({i}), expected {_actual}, but got {_}"
        assert _actual == (
            _ := cached_fact(i)
        ), f"Wrong output for cached_fact({i}), expected {_actual}, but got {_}"


if __name__ == "__main__":
    main(0, 10000, 2)
