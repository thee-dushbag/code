from math import log as _log, log2, floor
from typing import Callable
from fractions import Fraction
from mpack.timer import timer


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


def mpow(base: float, exp: int, /) -> float:
    v = base
    for _ in range(exp - 1):
        base *= v
    return base


def denom(base: float, tenth: int):
    last_y, cur_y = base, base / 2

    def inrange(base):
        upb, lwb = base + 0.01, base - 0.01
        return lambda cur: upb > cur > lwb

    found = inrange(base)
    while not found(cur_v := mpow(cur_y, tenth)):
        extent, last_y = abs(last_y - cur_y) / 2, cur_y
        if cur_v > base:
            cur_y -= extent
        elif cur_v < base:
            cur_y += extent
        else:
            break
    return cur_y


def apow(base: float, power: float, /) -> float:
    frac = Fraction(power)
    return mpow(denom(base, frac.denominator), frac.numerator)
