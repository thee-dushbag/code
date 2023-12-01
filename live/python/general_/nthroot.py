from time import sleep
import typing as ty
import click, math
from dataclasses import dataclass

_Tester: ty.TypeAlias = ty.Callable[[float], bool]

DELAY: float = 0.5
DECAY_FACTOR: float = 2
GROWTH_FACTOR: float = 2


@dataclass
class _Range:
    urange: float
    lrange: float


def _create_range(x: float, r: _Range, /) -> _Tester:
    ub, lb = x + r.urange, x - r.lrange
    print(f"Tester: upper_bound={ub} lower_bound={lb} {x=} {r=}")
    return lambda s: ub >= s >= lb


# def sqrt(x: float, r: _Range, /) -> float:
#     inrange = _create_range(x, r)
#     last_y, cur_y, counter = x, x / DECAY_FACTOR, 0
#     while not inrange((cur_sqr := cur_y ** 2)):
#         t = last_y
#         extent, last_y = abs(cur_y - last_y) / DECAY_FACTOR, cur_y
#         print(f"{counter} {cur_y=:.4f} last_y={t:.4f} {extent=:.4f} {cur_sqr=}")
#         if cur_sqr > x: cur_y -= extent
#         elif cur_sqr < x: cur_y += extent
#         else: break
#         counter += 1
#         sleep(DELAY)
#     return cur_y



def nthroot(x: float, n: float, r: _Range, /, *, factor: float = DECAY_FACTOR) -> float:
    inrange = _create_range(x, r)
    last_y, cur_y, counter = x, x / factor, 0
    while not inrange((cur_nthp := pow(cur_y, n))):
        t = last_y
        extent, last_y = abs(cur_y - last_y) / factor, cur_y
        print(f"{counter} {cur_y=:.15f} last_y={t:.15f} {extent=:.15f} {cur_nthp=:.15f}")
        if cur_nthp > x: cur_y -= extent
        elif cur_nthp < x: cur_y += extent
        else: break
        counter += 1
        sleep(DELAY)
    return cur_y


def _test_nthroot_impl(n: float, test_range: ty.Iterable[float]):
    from mpack.stream import Stream

    i = 6
    ac = pow(10, -i)
    r = _Range(ac, ac)
    with Stream():
        for x in test_range:
            v = round(pow(10, math.log10(x) / n), i + 1)
            m = round(nthroot(x, n, r), i + 1)
            cr = _create_range(v, r)
            assert cr(m), f"Failed at {x=} on {n=}, {v} != {m} at accuracy {ac}"


def test_nthroot():
    global DECAY_FACTOR, DELAY
    DELAY, DECAY_FACTOR = 0, 2
    for i in range(1, 5):
        _test_nthroot_impl(i, range(1, 5000))


@click.command
@click.argument("x", type=float)
@click.option("--delay", "-d", default=DELAY, type=float)
@click.option("--urange", "-U", default=0.005, type=float)
@click.option("--lrange", "-L", default=0.005, type=float)
@click.option("--root", "-n", default=2, type=float)
@click.option("--factor", "-f", default=DECAY_FACTOR, type=float)
def main(
    x: float, delay: float, factor: float, root: float, urange: float, lrange: float
):
    global DELAY
    DELAY = delay
    range = _Range(urange, lrange)
    click.echo(f"nthroot{x, root} = {nthroot(x, root, range, factor=factor)}")


if __name__ == "__main__":
    main()
