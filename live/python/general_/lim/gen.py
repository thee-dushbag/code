from typing import Callable, Generator, Iterable, Literal, TextIO, TypeVar
import more_itertools as mt
from string import ascii_uppercase
from itertools import permutations

T = TypeVar("T")


def names(n: int):
    return (f"_{i}" for i in range(1, n + 1))


def take(n: int, iterable: Iterable[T]) -> Generator[T, None, int]:
    count = 0
    if n > 0:
        for count, item in enumerate(iterable, start=1):
            yield item
            if count >= n:
                break
    return count


def letters(n: int) -> Generator[str, None, None]:
    for count in range(1, 27):
        perms = permutations(ascii_uppercase, count)
        n -= yield from take(n, map("".join, perms))
        if n <= 0:
            break


def create(n: int, *, b: int = 15, t: str = "", r: str = "", names=names):
    t = f": {t}" if t else t
    r = f" -> {r}" if r else r
    args = ", ".join(map(lambda n: n + t, names(n)))
    stmts = ["def function(%s)%s:" % (args, r)]
    all_names = list(names(n))
    last = all_names[-1]
    while len(all_names) > 1:
        new_names = []
        batches = mt.batched(all_names, b)
        for name, batch in zip(names(n), batches):
            stmt = f'{name} = {" + ".join(batch)}'
            stmts.append(stmt)
            new_names.append(name)
        all_names = new_names
    stmts.append(f"print({last})")
    stmts.append(f"return {all_names.pop()}")
    return "\n\t".join(stmts) + "\n"


def simple(n: int, names=names):
    last = ""

    def setlast(item: str) -> str:
        nonlocal last
        last = item
        return item

    args = ", ".join(map(setlast, names(n)))
    decl = "def function(%s):\n" % args
    body = "\treturn %s\n" % last
    return decl + body


NameGen = Callable[[int], Iterable[str]]
ContentGen = Callable[[int, NameGen], Iterable[str]]


def argskw(n: int, k: int, names: NameGen):
    gnames = names(n)
    yield from map(lambda v, _: str(v), range(1, n - k + 1), gnames)
    yield from map(lambda a, b: f"{a}={b}", gnames, range(n - k + 1, n + 1))

    # values = map(lambda a, b: f"{a}={b}", gnames, range(n - k + 1, n + 1))
    # values = list(values)
    # from random import shuffle
    # shuffle(values)
    # yield from values


def call(n: int, kp: float, names: NameGen = names):
    assert 0 <= kp <= 1, kp
    decl = "def caller():\n"
    args = ", ".join(argskw(n, round(n * kp), names))
    stmt = "\tresult = function(%s)\n" % args
    show = "\tprint(result)\n"
    body = '\nif __name__ == "__main__":\n\tcaller()\n'
    return decl + stmt + show + body


import click


def long_gen(n: int, gen: NameGen):
    return create(n, names=gen)


def short_gen(n: int, gen: NameGen):
    return simple(n, names=gen)


GenTypes = Literal["short", "long"]
content_gens: dict[GenTypes, ContentGen] = dict(short=short_gen, long=long_gen)


@click.command
@click.option("-n", type=click.IntRange(min=0), default=26)
@click.option("--file", "-f", type=click.File("w"), default="big.py")
@click.option("--gen", "-g", type=click.Choice(["short", "long"]))
@click.option("gen", "--short", "-s", flag_value="short", default=True)
@click.option("gen", "--long", "-l", flag_value="long")
@click.option(
    "--kwargs", "-k", type=click.IntRange(min=0, max=100, clamp=True), default=50
)
def main(n: int, file: TextIO, gen: GenTypes, kwargs: int):
    content_gen = content_gens[gen](n, letters)
    mt.consume(mt.side_effect(file.write, content_gen))
    file.write("\n%s" % call(n, kwargs / 100, letters))


if __name__ == "__main__":
    main()
