import itertools as it
from functools import partial
from math import sqrt
from typing import Any, Callable, Iterable, Optional, Sequence

import more_itertools as mit
from rich.console import Console

console = Console()
print = console.print


def _format(format_str: str, *args, **kwargs):
    return format_str.format(*args, **kwargs)


def is_sqr(x: int) -> bool:
    root: int = int(sqrt(x))
    return pow(root, 2) == x


def is_less_than(n: int, eq: bool = False):
    op = "<=" if eq else "<"

    def _impl(x: int) -> bool:
        return eval(f"{x}{op}{n}")

    return _impl


def e_or_o(num: int):
    return "even" if num % 2 == 0 else "odd"


IteratorCallback = Callable[[int, Any], Any]


def int_accumulator(cur: int = 0, init: int = 0):
    return cur + init


def callback_function(iterable: Iterable):
    def _impl(
        callback: IteratorCallback,
        accumulator: Callable[[Optional[Any], Optional[Any]], Any],
    ):
        initial = accumulator()
        for index, value in enumerate(iterable):
            callback(index, value)
            initial = accumulator(index + value, initial)
        return initial

    return _impl


def sep_floating_point(number: float):
    whole, _, decimal = str(number).partition(".")
    return int(whole), int(decimal) if decimal else 0


def add_comma(number: str, *, n: int = 3, grp_sep: str = ",", val_sep: str = ""):
    _v = mit.batched(mit.always_reversible(number), n)
    _v = mit.always_reversible(_v)
    _v = (mit.always_reversible(_g) for _g in _v)
    _v = (tuple(_g) for _g in _v)
    _v = (val_sep.join(_g) for _g in _v)
    return grp_sep.join(_v)


def comma_sep(number: float):
    whole, decimal = sep_floating_point(number)
    whole = add_comma(str(whole))
    return f"{whole}.{decimal}" if type(number) == float else f"{whole}"


def itertools_():
    adj = _format("Adjacent to true:\n {}", tuple(mit.adjacent(is_sqr, range(0, 11))))
    data = 1, 2, 3, 4
    adj = _format("All_Equal: {} : {}", data, mit.all_equal(data))
    adj = _format("All_Unique: {} : {}", data, mit.all_unique(data))
    adj = _format(
        "Always_Iterable: {} : {}", data, tuple(mit.always_iterable(data, None))
    )
    adj = _format(
        "Always_Reversible: {} : {}", data, tuple(mit.always_reversible(data))
    )
    data = "".join(str(i) for i in range(1, 10)), 3
    adj = _format("batched: {} : {}", data[0], tuple(mit.batched(data[0], data[1])))
    data = range(10), 6
    adj = _format(
        "before_and_after: {} : {}",
        data,
        tuple(
            tuple(x) for x in mit.before_and_after(is_less_than(data[1], True), data[0])
        ),
    )
    data = range(11)
    buckets = mit.bucket(data, e_or_o)
    adj = _format(
        "bucket: {} : {}", data, {key: tuple(buckets[key]) for key in ("even", "odd")}
    )
    data = range(1, 11)
    with mit.callback_iter(
        partial(callback_function(data), accumulator=int_accumulator)
    ) as accum:
        for args, kwargs in accum:
            # print(args, kwargs)
            pass
        adj = accum.result
    data = 87656789
    adj = _format("Number Separator: {} : {}", data, comma_sep(data))
    data = 1, 2, 3, 4, 5, 6, 7, 8, 9
    adj = _format("Chunked Even: {} : {}", data, tuple(mit.chunked_even(data, 2)))
    data = ["ab", ("cd", "ef"), ["gh", "ij"]]
    adj = list(mit.collapse(data))
    data = ["simon", "nganga", "njoroge"]
    adj = list(mit.circular_shifts(data))
    adj = list(list(x) for x in mit.consecutive_groups("abcde", "abcde".index))
    print(adj)


def main(argv: Sequence[str]) -> None:
    itertools_()


if __name__ == "__main__":
    from sys import argv

    main(argv[1:])
