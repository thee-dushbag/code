import math as _m
from mpack.timer import timer, TimeitResult
import typing as ty

_Tester: ty.TypeAlias = ty.Callable[[float], bool]
DECAY_FACTOR = 2


class _Range:
    def __init__(self, urange: float, lrange: float):
        self.urange: float = urange
        self.lrange: float = lrange


_default_accuracy: ty.Final[float] = 1e7
_default_range: ty.Final[_Range] = _Range(1 / _default_accuracy, 1 / _default_accuracy)


def _create_range(x: float, r: _Range, /) -> _Tester:
    ub, lb = x + r.urange, x - r.lrange
    return lambda s: ub >= s >= lb


def _create_pow_map(base: float, exp: int) -> tuple[float, dict[int, float], int]:
    mapping: dict[int, float] = {}
    rounds = _m.floor(_m.log2(exp))
    base, temp = 1, base
    for round in range(rounds):
        mapping[round] = temp
        base *= temp
        temp *= temp
    return base, mapping, exp - (2**rounds - 1)


def _create_growing_pow_map(
    base: float, exp: int
) -> tuple[float, dict[int, tuple[float, int]], int]:
    cache: dict[int, tuple[float, int]] = {}
    rounds = _m.floor(_m.log2(exp))
    temp, base, exp_decay = base, 1, 1
    for round in range(rounds):
        base *= temp
        temp *= temp
        exp_decay *= 2
        cache[round] = base, exp_decay - 1
    exp -= cache[rounds - 1][1]
    return base, cache, exp


def _compute_from_map(mapping: dict[int, float], exp: int) -> float:
    base = mapping[0]
    if exp == 0:
        return 1
    elif exp == 1:
        return base
    rounds = _m.floor(_m.log2(exp))
    for round in range(1, rounds):
        base *= mapping[round]
    exp -= 2**rounds - 1
    return base * _compute_from_map(mapping, exp)


def _compute_from_growing_map(cache: dict[int, tuple[float, int]], exp: int) -> float:
    cur = cache[0]
    base = cur[0]
    while exp > 1:
        rounds = _m.floor(_m.log2(exp))
        cur = cache[rounds - 1]
        base *= cur[0]
        exp -= cur[1]
    return base


def int_exp(base: float, exp: int, /) -> float:
    if exp == 0:
        return 1
    elif exp == 1:
        return base
    base, map, exp = _create_pow_map(base, exp)
    return base * _compute_from_map(map, exp)


def int_exp_growing(base: float, exp: int, /) -> float:
    if exp == 0:
        return 1
    elif exp == 1:
        return base
    base, cache, exp = _create_growing_pow_map(base, exp)
    return base * _compute_from_growing_map(cache, exp)


def int_exp_denom(
    x: float, n: int, /, r: _Range = _default_range, *, factor: float = DECAY_FACTOR
) -> float:
    if n == 0:
        return 1
    elif n == 1:
        return x
    inrange = _create_range(x, r)
    last_y, cur_y, counter = x, x / factor, 0
    while not inrange(cur_nthp := int_exp(cur_y, n)):
        extent, last_y = abs(cur_y - last_y) / factor, cur_y
        if cur_nthp > x:
            cur_y -= extent
        elif cur_nthp < x:
            cur_y += extent
        else:
            break
        counter += 1
    return cur_y


def _simplify(n1: int, n2: int, /) -> tuple[int, int]:
    v = _m.gcd(n1, n2)
    return n1 // v, n2 // v


def power(x: float, y: float, /, accuracy: _Range = _default_range) -> float:
    num, den = _m.floor(y * _default_accuracy), _m.floor(_default_accuracy)
    num, den = _simplify(num, den)
    x = int_exp_denom(x, den, accuracy)
    return int_exp(x, num)


def _basic_pow(base: float, exp: int, /) -> float:
    temp, base = base, 1
    for _ in range(exp):
        base *= temp
    return base


def test_int_exp():
    from pypow import pow as cpow

    for i in range(1, 100, 2):
        for j in range(1, 1000, 3):
            powered = i**j
            assert powered == int_exp(i, j)
            # assert powered == _basic_pow(i, j)
            assert powered == int_exp_growing(i, j)
            assert powered == cpow(i, j)


def average(times: list[TimeitResult]) -> tuple[float, float]:
    total = sum(time.lapse.time for time in times)
    return (total / len(times)), total


def pow_benchmarks():
    from sys import set_int_max_str_digits  # type: ignore
    from pypow import pow as cpow

    set_int_max_str_digits(10000)
    from tqdm import tqdm

    def run_test(power) -> tuple[float, float]:
        return average(
            [power(i, j) for i in tqdm(range(100, 10000, 3)) for j in range(1, 1000, 2)]
        )

    # basic_pow = timer(_basic_pow)
    cpow_exp = timer(cpow)
    int_exp_pow = timer(int_exp)
    int_exp_gpow = timer(int_exp_growing)
    # power_pow = timer(power)
    builtin_pow = timer(pow)
    bpow_avg, bpow_total = run_test(builtin_pow)
    cpow_avg, cpow_total = run_test(cpow_exp)
    iexp_gavg, iexp_gtotal = run_test(int_exp_gpow)
    iexp_avg, iexp_total = run_test(int_exp_pow)
    # power_pow_total, power_pow_avg = run_test(power_pow)
    # basic_avg, basic_total = run_test(basic_pow)
    print(
        f"BuiltinPow took a total of {bpow_total} total and {bpow_avg} average seconds."
    )
    print(f"C++Pow took a total of {cpow_total} total and {cpow_avg} average seconds.")
    # print(f"PowerFloat took a total of {power_pow_total} total and {power_pow_avg} average seconds.")
    print(
        f"IntExpPowGrowing took a total of {iexp_gtotal} total and {iexp_gavg} average seconds."
    )
    print(
        f"IntExpPow took a total of {iexp_total} total and {iexp_avg} average seconds."
    )
    # print(f"BasicPower took a total of {basic_total} total and {basic_avg} average seconds.")


if __name__ == "__main__":
    pow_benchmarks()
