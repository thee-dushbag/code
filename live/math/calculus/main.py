from typing import Sequence
import sym, sympy as sy
from mpack import print

sy.init_printing(use_unicode=True, latex_mode='equation*')
pri = sy.pretty_print


def main(argv: Sequence[str]) -> None:
    func = sym.x ** 2
    pri(func)
    arcl = sym.arc_length(func)
    pri(arcl)
    saf = sym.surface_area(func)
    pri(saf)
    vol = sym.volume(func)
    pri(vol)
    a, b = -3, 4
    print(f"S.A: func{a,b} => {sym.fsubrange(saf, sym.x, a, b)}")
    print(f"Vol: func{a,b} => {sym.fsubrange(vol, sym.x, a, b)}")


if __name__ == '__main__':
    from sys import argv
    main(argv[1:])