from math import log as _log
from typing import Callable


def _gcd(a: int, b: int):
    if b == 0:
        return a
    return _gcd(b, a % b)


def gcd(a: int, b: int):
    a, b = abs(a), abs(b)
    a, b = (a, b) if a >= b else (a, b)
    return _gcd(a, b)


def root(n: float, /, *, base: float | None = None) -> Callable[[float], float]:
    base = base or 10
    return lambda x: base ** (_log(x, base=base) / n)


def nthrt(x: float, /, n: float, *, base: float | None = None) -> float:
    return root(n, base=base)(x)
