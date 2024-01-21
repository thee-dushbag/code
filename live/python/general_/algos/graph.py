people = {
    "simon": ["faith", "lydia", "darius", "makori"],
    "lydia": ["simon", "faith", "wairimu", "puss"],
    "makori": ["simon", "darius", "obed"],
    "obed": ["darius", "makori", "ngor"],
    "ngor": ["obed", "brayo"],
    "faith": ["simon", "lydia"],
    "brayo": ["nike", "ngor"],
    "darius": ["simon", "matandi", "obed"],
    "matandi": ["losuru", "darius", "wandera"],
    "wandera": ["makori"],
    "wairimu": ["puss"],
    "puss": ["lydia"],
    "losuru": ["matandi", "obed"],
}

infinity = float("inf")

graph = {
    "A": [("B", 5), ("C", 2)],
    "B": [("D", 4), ("E", 2)],
    "C": [("B", 8), ("E", 7)],
    "D": [("E", 6), ("F", 3)],
    "E": [("F", 1)],
    "F": [],
}

import typing as ty

GraphType = dict["str", list[tuple[str, int]]]


class Node:
    def __init__(self, parent: str, weight: float | None = None) -> None:
        self.weight: float = weight or infinity
        self.parent: str = parent
        self._checked = False

    @property
    def checked(self) -> bool:
        return self._checked

    def check(self):
        self._checked = True

    def __str__(self) -> str:
        return f"Node({self.parent!r}, {self.weight})"

    __repr__ = __str__


def get_lowest_node(nodes: dict[str, Node]):
    smallest_name = ty.cast(str, None)
    smallest = Node(smallest_name)
    for name, node in nodes.items():
        if node.weight < smallest.weight and not node.checked:
            smallest_name = name
            smallest = node
    return smallest_name, smallest


def djikstras_search(graph: GraphType, start: str, stop: str):
    nodes = {node: Node(start, weight) for node, weight in graph[start]}
    name, node = get_lowest_node(nodes)
    while name is not None:
        nearest = graph[name]
        node.check()
        for _name, weight in nearest:
            _node = nodes.setdefault(_name, Node(name))
            _weight = node.weight + weight
            if _weight < _node.weight:
                _node.weight = _weight
                _node.parent = name
        name, node = get_lowest_node(nodes)
        if stop in nodes and name == stop:
            break
    path = [stop]
    weight = nodes[stop].weight
    while stop != start:
        node = nodes[stop].parent
        path.append(node)
        stop = node
    path.reverse()
    return path, weight


def breadth_first_search(person: str, target: str):
    batch = people[person].copy()
    seen = {person}
    steps = 0
    while batch:
        queue, batch = batch, []
        steps += 1
        while queue:
            current = queue.pop(0)
            if current in seen:
                continue
            if current == target:
                return steps
            batch += people[current]
            seen.add(current)
