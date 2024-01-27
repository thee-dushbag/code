import random, json, math, heapq, click
from collections import defaultdict
import dataclasses as dt

Range = tuple[int, int]
FILE = "fruits.json"
KEY = "fruits"
RANGE: Range = (0, 10000)
MID = int(RANGE[1] / 2)
ORANGES: Range = (1, MID)
GRAPES: Range = (MID + 1, RANGE[1])


@dt.dataclass
class Fruit:
    name: str
    color: int
    size: int


def create_fruit(name: str, size: Range, color: Range) -> Fruit:
    cr = random.randint(*color)
    sz = random.randint(*size)
    return Fruit(name, cr, sz)


def create_fruits(count: int, name: str, size: Range, color: Range) -> list[Fruit]:
    return [create_fruit(name, size, color) for _ in range(count)]


def gen_fruits(count: int):
    osize = int(count / 2)
    gsize = count - osize
    oranges = create_fruits(osize, "orange", ORANGES, ORANGES)
    grapes = create_fruits(gsize, "grape", GRAPES, GRAPES)
    fruits = [*oranges, *grapes]
    random.shuffle(fruits)
    return fruits


def load_fruits(*, file: str | None = None, key: str | None = None) -> list[Fruit]:
    key = KEY if key is None else key
    file = FILE if file is None else file
    with open(file, "r") as f:
        fruits = json.load(f).get(key, [])
    return [Fruit(*fruit) for fruit in fruits]


def save_fruits(
    fruits: list[Fruit] | tuple[Fruit, ...],
    *,
    key: str | None = None,
    file: str | None = None,
):
    _fruits = [dt.astuple(fruit) for fruit in fruits]
    key = KEY if key is None else key
    file = FILE if file is None else file
    with open(file, "w") as f:
        json.dump({key: _fruits}, f)


def _fruit_distance(fruit1: Fruit, fruit2: Fruit) -> float:
    return math.hypot(fruit1.size - fruit2.size, fruit1.color - fruit2.color)


class _Distance:
    def __init__(self, fruit: Fruit, distance: float) -> None:
        self.fruit = fruit
        self.distance = distance

    def __eq__(self, fruit: "_Distance") -> bool:
        return self.distance == fruit.distance

    def __lt__(self, fruit: "_Distance") -> bool:
        return self.distance < fruit.distance


def min_distance(target: Fruit, *fruits: Fruit, k: int | None = None) -> list[Fruit]:
    k = 3 if k is None else k
    assert len(fruits) >= k
    dists: list[_Distance] = []
    for fruit in fruits:
        dist = _fruit_distance(target, fruit)
        heapq.heappush(dists, _Distance(fruit, dist))
    dists = [heapq.heappop(dists) for _ in range(k)]
    return [fruit.fruit for fruit in dists]


def common_fruit(fruits: list[Fruit]):
    count: defaultdict[str, int] = defaultdict(lambda: 0)
    for fruit in fruits:
        count[fruit.name] += 1
    lcount = [(name, cnt) for name, cnt in count.items()]
    return max(lcount, key=lambda f: f[1])[0]


def guess_fruit(fruits: list[Fruit], k: None | int = None, /):
    try:
        while True:
            point = input("point[size,color]: ")
            if point == "exit":
                break
            size, _, color = point.partition(",")
            if not size.isnumeric():
                print(f"Error: size must be an integer, got {size!r}")
                continue
            if not color.isnumeric():
                print(f"Error: color must be an integer, got {color!r}")
                continue
            isize, icolor = int(size), int(color)
            if 0 > isize or isize > RANGE[1]:
                print(f"Error: size must be in the range of {RANGE}, got {isize}")
                continue
            if 0 > icolor or icolor > RANGE[1]:
                print(f"Error: color must be in the range of {RANGE}, got {icolor}")
                continue
            fruit = Fruit("unknown", icolor, isize)
            nearest = min_distance(fruit, *fruits, k=k)
            fruit.name = common_fruit(nearest)
            print("Guess:", fruit)
    except KeyboardInterrupt:
        ...
    finally:
        print("Bye")


def add_fruit(fruits: list[Fruit], size: Range, color: Range, k: int | None = None):
    icolor, isize = random.randint(*color), random.randint(*size)
    fruit = Fruit("unknown", icolor, isize)
    nearest = min_distance(fruit, *fruits, k=k)
    fruit.name = common_fruit(nearest)
    fruits.append(fruit)
    return fruit


def add_fruits(
    count: int, fruits: list[Fruit], size: Range, color: Range, k: int | None = None
):
    for _ in range(count):
        add_fruit(fruits, size, color, k=k)
    return fruits


def plot_fruits(fruits: list[Fruit]):
    import matplotlib.pyplot as plt

    colors = dict(orange=[], grape=[])
    sizes = dict(orange=[], grape=[])
    for fruit in fruits:
        colors[fruit.name].append(fruit.color)
        sizes[fruit.name].append(fruit.size)

    plt.scatter(sizes["orange"], colors["orange"], color=(1, 165 / 255, 0), marker="*")
    plt.scatter(sizes["grape"], colors["grape"], color=(0.5, 0, 0.5), marker="+")
    plt.grid(visible=True, which="both")
    plt.title("Oranges vs Grapes")
    plt.ylabel("Color")
    plt.xlabel("Size")
    plt.show()


@click.group
@click.help_option("--help", "-h")
def cli():
    ...


@cli.command
@click.option(
    "--file",
    "-f",
    default=FILE,
    type=click.Path(exists=True, readable=True, dir_okay=False, file_okay=True),
)
@click.help_option("--help", "-h")
def plot(file: str):
    fruits = load_fruits(file=file)
    plot_fruits(fruits)


@cli.command
@click.option(
    "--file",
    "-f",
    default=FILE,
    type=click.Path(dir_okay=False, writable=True, file_okay=True),
)
@click.option("--base", "-b", type=int, default=60)
@click.option("--add", "-a", type=int, default=140)
@click.option("--k", "-k", type=int, default=3)
@click.help_option("--help", "-h")
def gen(base: int, add: int, k: int, file: str):
    fruits = gen_fruits(base)
    add_fruits(add, fruits, RANGE, RANGE, k=k)
    save_fruits(fruits, file=file)


@cli.command
@click.option("--k", "-k", type=int, default=5)
@click.option(
    "--file",
    "-f",
    default=FILE,
    type=click.Path(exists=True, readable=True, dir_okay=False, file_okay=True),
)
@click.help_option("--help", "-h")
def play(k: int, file: str):
    fruits = load_fruits(file=file)
    guess_fruit(fruits, k)


if __name__ == "__main__":
    cli()
