import typing as ty
import random as rand
from time import sleep


@ty.final
class sides:
    none: ty.Final[int] = 0
    up: ty.Final[int] = 1
    right: ty.Final[int] = 2
    down: ty.Final[int] = 4
    left: ty.Final[int] = 8


BLOCKS_MAP: ty.Final = dict(
    # Empty
    # blank=sides.none,
    # Coners
    bottom_right=sides.down | sides.right,
    bottom_left=sides.down | sides.left,
    up_right=sides.up | sides.right,
    up_left=sides.up | sides.left,
    # Lines
    right_left=sides.right | sides.left,
    up_down=sides.up | sides.down,
    # T-shapes
    bottom_t=sides.down | sides.right | sides.left,
    up_t=sides.up | sides.right | sides.left,
    right_t=sides.right | sides.up | sides.down,
    left_t=sides.left | sides.up | sides.down,
    # Cross
    cross=sides.left | sides.right | sides.up | sides.down,
)

SIDES_MATRIX_IDX: ty.Final = {
    1: sides.up,
    5: sides.right,
    7: sides.down,
    3: sides.left,
}

BLOCKS: ty.Final = list(BLOCKS_MAP.values())
ENTROPY_MAX: ty.Final = len(BLOCKS) + 1

SIDES: ty.Final = list(SIDES_MATRIX_IDX.values())
COMPATIBLE_SIDES: ty.Final = {
    sides.up: sides.down,
    sides.down: sides.up,
    sides.left: sides.right,
    sides.right: sides.left,
    sides.none: sides.none,
}


def _connectable(block: int, block1: int, side: int) -> bool:
    return bool(block & side) == bool(block1 & COMPATIBLE_SIDES[side])


def _connectable_blocks_helper(block: int, side: int, blocks: list[int] | None = None):
    blocks = BLOCKS if blocks is None else blocks
    return [blk for blk in blocks if _connectable(block, blk, side)]


def connectable_blocks(block: int, blocks: list[int] | None = None):
    return {side: _connectable_blocks_helper(block, side, blocks) for side in SIDES}


def creatematrix(dim: tuple[int, int], init):
    return [[init() for _ in range(dim[1])] for _ in range(dim[0])]


def index2shape(shape: tuple[int, int]):
    def shaper(index: int):
        return index // shape[1], index % shape[1]

    return shaper


CHAR_BLOCK_MAP = dict(
    bottom_right="┌",
    bottom_left="┐",
    up_right="┘",
    up_left="└",
    blank=" ",
    bottom_t="┬",
    left_t="┤",
    right_t="├",
    up_t="┴",
    up_down="|",
    right_left="-",
    cross="+",
)
CHAR_BLOCK = {BLOCKS_MAP[block]: CHAR_BLOCK_MAP[block] for block in BLOCKS_MAP}


def createtile_matrix(block: int, o=None, e=None):
    # return CHAR_BLOCK.get(block, '▓')
    empty, occupied = e or " ", o or "█"
    if int(block) == -1:
        return creatematrix((3, 3), lambda: "✸")
    matrix = creatematrix((3, 3), lambda: empty)
    if int(block) == sides.none:
        return matrix
    matrix[1][1] = occupied
    shaper = index2shape((3, 3))

    for index, side in SIDES_MATRIX_IDX.items():
        if int(block) & side == side:
            row, col = shaper(index)
            matrix[row][col] = occupied
    return matrix


def drawtiles(*tiles, rsep="", bsep="", esep=""):
    matrices = (createtile_matrix(block) for block in tiles)
    for rows in zip(*matrices):
        print(bsep + rsep.join("".join(row) for row in rows) + esep)


class Neighbors:
    def __init__(
        self, *, up: "Pixel", right: "Pixel", left: "Pixel", down: "Pixel"
    ) -> None:
        self.up = up
        self.left = left
        self.down = down
        self.right = right

    def __iter__(self) -> ty.Generator[tuple[int, "Pixel"], None, None]:
        for sidename in "up", "right", "down", "left":
            yield getattr(sides, sidename), getattr(self, sidename)


class Pixel:
    def __init__(self, *, edgy: bool | None = None) -> None:
        self._value = None
        self._edgy = bool(edgy)
        self._possibles = set(BLOCKS)

    @property
    def edgy(self) -> bool:
        return self._edgy

    @property
    def value(self) -> int:
        return -1 if self._value is None else self._value

    @value.setter
    def value(self, val: int) -> None:
        assert isinstance(val, int), f"expected val to be an integer"
        assert self._value is None, f"This block has already been taken"
        self._possibles = {val}
        self._value = val

    @property
    def entropy(self) -> int:
        return ENTROPY_MAX if self.occupied else len(self._possibles)

    def collapse(self):
        if not self.occupied:
            if not self._possibles:
                self.value = -1
            else:
                self.value = rand.choice(list(self._possibles))

    def update(self, neighbors: Neighbors):
        psbles = self._possibles
        for side, neighbor in neighbors:
            if neighbor.occupied:
                cside = COMPATIBLE_SIDES[side]
                targets = set(connectable_blocks(neighbor.value)[cside])
                psbles.intersection_update(targets)
        self._possibles = psbles

    @property
    def occupied(self) -> bool:
        return self._value is not None

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return f"Pixel({self._value}, entropy={self.entropy}, edgy={self._edgy}, sp={self._possibles})"

    __repr__ = __str__


class Picture:
    def __init__(self, shape: tuple[int, int] | int) -> None:
        if isinstance(shape, int):
            shape = (shape, shape)
        self._shape = shape
        self._size = shape[0] * shape[1]
        assert self._size > 0, f"The picture matrix is empty"
        self._matrix = [Pixel() for _ in range(self._size)]

    def create(self, verbose: bool = False):
        root = rand.choice(self._matrix)
        self._collapse_pixel(root)
        # self.show(verbose)
        while True:
            pixel = self.getmin_entropy()
            if pixel is None:
                break
            self._collapse_pixel(pixel)
            # sleep(0.01)
            # print("\033[H\033[2J\033[3J")
            # self.show(verbose)

    def _collapse_pixel(self, pixel: Pixel):
        assert not pixel.occupied, f"Cannot collapse a collapsed pixel."
        pixel.collapse()
        index = self._matrix.index(pixel)
        row, column = self._index2shape(index)
        neighbors = self.getneighbors(row, column)
        for _, neighbor in neighbors:
            if neighbor.edgy:
                continue
            index = self._matrix.index(neighbor)
            row, column = self._index2shape(index)
            others = self.getneighbors(row, column)
            neighbor.update(others)

    def _index2shape(self, index: int) -> tuple[int, int]:
        return index // self._shape[0], index % self._shape[1]

    def show(self, verbose: bool = False):
        line = bsep = esep = rsep = ""
        if verbose:
            line = "------" * self._shape[1] + "-\n"
            rsep = " | "
            bsep = "| "
            esep = " |"

        print(line, end="")
        for row in range(self._shape[0]):
            drawtiles(
                *(
                    pixel.value
                    for pixel in self._matrix[
                        row * self._shape[0] : row * self._shape[0] + self._shape[1]
                    ]
                ),
                rsep=rsep,
                bsep=bsep,
                esep=esep,
            )
            print(line, end="")

    def getmin_entropy(self) -> Pixel | None:
        matrix = sorted(self._matrix, key=lambda p: p.entropy)
        lowest = matrix[0].entropy
        if lowest == ENTROPY_MAX:
            return
        for index, pixel in enumerate(matrix):
            if pixel.entropy != lowest:
                matrix = matrix[:index]
                break
        pixel = rand.choice(matrix)
        return pixel

    def getpixel(self, row: int, column: int) -> Pixel:
        index = row * self._shape[0] + column
        if (
            index >= self._size
            or index < 0
            or row < 0
            or row >= self._shape[0]
            or column < 0
            or column >= self._shape[1]
        ):
            return Pixel(edgy=True)
        return self._matrix[index]

    def getneighbors(self, row: int, column: int) -> Neighbors:
        return Neighbors(
            up=self.getpixel(row - 1, column),
            down=self.getpixel(row + 1, column),
            left=self.getpixel(row, column - 1),
            right=self.getpixel(row, column + 1),
        )

    def __len__(self) -> int:
        return self._size


if __name__ == '__main__':
    picture = Picture(55)
    picture.create()
    picture.show()
