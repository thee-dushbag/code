#!/bin/env python

import typing as ty, sys


class Size:
    def __init__(self, size: int):
        self.total = size
        self.bytes = size & 1023
        self.kilo_bytes = (size >> 10) & 1023
        self.mega_bytes = (size >> 20) & 1023
        self.giga_bytes = (size >> 30) & 1023
        self.tera_bytes = (size >> 40) & 1023
        self.peta_bytes = (size >> 50) & 1023
        self.exa_bytes = (size >> 60) & 1023
        self.yotta_bytes = (size >> 70) & 1023
        self.zetta_bytes = size >> 80


def main(sizes: ty.Iterable[int]):
    for size in map(Size, sizes):
        for name, value in reversed(size.__dict__.items()):
            if name.endswith("bytes") and value > 0:
                print(f"{value}{name[0]} ", end="")
        print(f" -  {size.total}")


if __name__ == "__main__":
    main(map(lambda v: int(eval(v)), sys.argv[1:]))
