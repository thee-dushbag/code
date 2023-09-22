from typing import Any, Callable


class Set:
    """A set that store no elements."""

    def __init__(self, *, include=None, exclude=None, properties=None):
        self.include = set(include) if include else set()
        self.exclude = set(exclude) if exclude else set()
        self.properties = set(properties) if properties else set()

    def check_valid(self):
        assert not (
            common := set(self.include).intersection(self.exclude)
        ), f"Elements {common} appear in both exclude and include set."
        if self.include:
            assert all(
                all(prop(elem) for elem in self.include) for prop in self.properties
            ), f"Some elements in the include do not conform to some/all properties: {self.include}"
        if self.exclude:
            assert any(
                all(prop(elem) for elem in self.exclude) for prop in self.properties
            ), f"Some elements in the exclude do conform to all properties: {self.exclude}"

    def add_include(self, element):
        self.include.add(element)

    def add_exclude(self, element):
        self.exclude.add(element)

    def add_property(self, prop: Callable[[Any], bool], prop_name=None):
        if prop_name:
            prop.__name__ = prop_name
        self.properties.add(prop)

    def is_element_of(self, element: Any):
        if element in self.include:
            return True
        if element in self.exclude:
            return False
        if self.properties:
            return all(prop(element) for prop in self.properties)
        return False

    def union(self, other: "Set"):
        includes = self.include.union(other.include)
        excludes = self.exclude.union(other.exclude)
        properties = self.properties.union(other.properties)
        return Set(include=includes, exclude=excludes, properties=properties)

    def intersect(self, other: "Set"):
        includes = self.include.intersection(other.include)
        excludes = self.exclude.intersection(other.exclude)
        properties = self.properties.intersection(other.properties)
        return Set(include=includes, exclude=excludes, properties=properties)

    def __str__(self):
        prop_names = set(prop.__name__ for prop in self.properties)
        return f"Set(include={self.include}, exclude={self.exclude}, properties={prop_names})"

    def __repr__(self) -> str:
        return str(self)
