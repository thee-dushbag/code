from typing import Sequence

from descriptors import Property
from rich.console import Console

console = Console()
print = console.print


class Operate:
    def __init__(self, value) -> None:
        self.value = value

    @Property
    def cube(self):
        return self.value**3

    @Property
    def square(self):
        return self.value**2

    @square.setter
    def square(self, sqr_root):
        self.value = pow(sqr_root, 1 / 2)

    @cube.setter
    def cube(self, cube_root):
        self.value = pow(cube_root, 1 / 3)

    @cube.deleter
    def cube(self):
        print("Deleting cube")

    @square.deleter
    def square(self):
        print("Deleting square")


def main(argv: Sequence[str]) -> None:
    op = Operate(5)
    op.square = 100
    print(op.square)
    print(op.cube)
    del op.cube
    op.cube = 8
    print(op.square)
    print(op.cube)


if __name__ == "__main__":
    from sys import argv

    main(argv[1:])
