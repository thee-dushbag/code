from utils import load, dump, Route, Path, Point
from itertools import permutations, pairwise, combinations
import heapq


def shortest_path_best(points: list[Point]):
    shortest = float("inf")
    path: list[Point] = []
    for route in permutations(points):
        distance = 0
        for p1, p2 in pairwise(route):
            distance += p1 @ p2
        if distance < shortest:
            shortest = distance
            path = list(route)
    edges: list[Path] = []
    for p1, p2 in pairwise(path):
        edges.append(Path(p1, p2))
    return Route(edges)


def _shortest_distance(points: list[Point]) -> tuple[Point, Point]:
    target: tuple[Point, Point] | None = None
    shortest = float("inf")
    for p1 in points:
        for p2 in points:
            if p1 is p2:
                continue
            distance = p1 @ p2
            if distance < shortest:
                target = p1, p2
                shortest = distance
    if target is None:
        raise Exception("No shortest between points.")
    return target


def _closest_neighbor(point: Point, points: list[Point], notinclude: set[Point]):
    shortest, target = float("inf"), None
    for neighbor in points:
        if neighbor == point or neighbor in notinclude:
            continue
        distance = neighbor @ point
        if distance < shortest:
            shortest = distance
            target = neighbor
    return target


def shortest_path_appr(points: list[Point]):
    start, finish = _shortest_distance(points)
    route = Route([Path(start, finish)])
    seen, stop = {start, finish}, set(points)
    while stop - seen:
        begin = _closest_neighbor(start, points, seen)
        end = _closest_neighbor(finish, points, seen)
        if begin is not None and end is not None:
            if begin @ start < end @ finish:
                point = begin
                _start = True
            else:
                point = end
                _start = False
        elif begin is not None:
            point = begin
            _start = True
        elif end is not None:
            point = end
            _start = False
        else:
            raise Exception("Unreachable.")

        if _start:
            route.addleft(Path(point, start))
            start = point
        else:
            route.add(Path(finish, point))
            finish = point
        seen.add(point)
    return route


inf = float("inf")


def _sorted_paths(points: list[Point]):
    heap: list[Path] = []
    for p1, p2 in combinations(points, 2):
        path = Path(p1, p2)
        heapq.heappush(heap, path)
    sorted: list[Path] = []
    while heap:
        path = heapq.heappop(heap)
        sorted.append(path)
    return sorted


def shortest_path_appr2(points: list[Point]):
    spaths = _sorted_paths(points)
    start = spaths.pop(0)
    beg, end = start.p1, start.p2
    route = Route([start])
    seen = {beg, end}
    total_paths = len(points) - 1
    while len(route.paths) < total_paths and spaths:
        for path in spaths:
            if end in (path.p1, path.p2):
                if path.p2 == end:
                    path.reverse()
                if path.p2 not in seen:
                    route.add(path)
                    end = path.p2
                spaths.remove(path)
                seen.add(end)
                break
            if beg in (path.p1, path.p2):
                if path.p1 == beg:
                    path.reverse()
                if path.p1 not in seen:
                    route.addleft(path)
                    beg = path.p1
                spaths.remove(path)
                seen.add(beg)
                break
    return route
