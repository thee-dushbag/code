# Greedy Algorithms

import math
import random
import string
import json


class Point:
    def __init__(self, name: str, x: float, y: float) -> None:
        self.name = name
        self.x = x
        self.y = y

    def distance(self, point: "Point") -> float:
        x = abs(self.x - point.x)
        y = abs(self.y - point.y)
        return round(math.hypot(x, y), 2)

    def __str__(self) -> str:
        return f"Point({self.name!r}, {self.x, self.y})"

    __repr__ = __str__
    __matmul__ = distance

    def __hash__(self) -> int:
        return hash(f"{self.name}({self.x}, {self.y})")

    def __eq__(self, point: "Point") -> bool:
        return self.name == point.name


class Map:
    def __init__(self, width: int | None = None, height: int | None = None) -> None:
        self.height = height or 100
        self.width = width or 100

    def genp(self, points: int) -> list[Point]:
        assert points <= 52, f"Not enough names for all these points. {points}"
        return [
            Point(
                string.ascii_letters[index],
                random.randrange(self.width + 1),
                random.randrange(self.height + 1),
            )
            for index in range(points)
        ]


def dump(points: int, file: str | None = None):
    m = Map(width=10000, height=10000)
    _points = m.genp(points)
    datap = {p.name: (p.x, p.y) for p in _points}
    _dist = {}
    for p in _points:
        dist = {}
        for n in _points:
            dist[n.name] = p @ n
        _dist[p.name] = dist

    data = dict(points=datap, distance=_dist)

    if file is not None:
        with open(file, "w") as f:
            json.dump(data, f, indent=2)
    return data


def load(
    *,
    file: str | None = None,
    data: dict[str, dict[str, float] | tuple[float, float]] | None = None,
):
    if file is None and data is None:
        raise Exception("Expected at least one: file or data.")
    if file is not None:
        with open(file) as f:
            data = json.load(f)
    if data is None:
        raise Exception("Data is None")
    distance = data["distance"]
    _points: dict[str, tuple[float, float]] = data["points"]  # type: ignore
    points = {name: Point(name, x, y) for name, (x, y) in _points.items()}
    return points, distance


class Path:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2

    def __hash__(self) -> int:
        p1, p2 = self.p1.name, self.p2.name
        if p1 > p2:
            p1, p2 = p2, p1
        return hash(p1 + p2)

    def __eq__(self, path: "Path") -> bool:
        return self.distance() == path.distance()

    def __lt__(self, path: "Path") -> bool:
        return self.distance() < path.distance()

    def distance(self) -> float:
        return round(self.p1 @ self.p2, 2)

    def __str__(self) -> str:
        return self.p1.name + self.p2.name

    __repr__ = __str__

    def reverse(self):
        self.p1, self.p2 = self.p2, self.p1

    __float__ = distance


class Route:
    def __init__(self, iterable=None) -> None:
        self.paths: list[Path] = []
        self.add = self.paths.append
        self.addleft = lambda path: self.paths.insert(0, path)
        self.clear = self.paths.clear
        self.pop = self.paths.pop
        self.extend = self.paths.extend
        if iterable is not None:
            self.extend(iterable)

    def __iadd__(self, path: Path):
        self.add(path)
        return self

    @property
    def distance(self):
        return sum(float(p) for p in self.paths)

    def __str__(self) -> str:
        paths = " -> ".join(map(str, self.paths))
        return f"Route({paths}, distance={self.distance})"

    __repr__ = __str__

    def reverse(self):
        for path in self.paths:
            path.reverse()
        self.paths.reverse()
