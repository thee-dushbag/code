"""
FLYWEIGHT DESIGN PATTERN
========================
The Flyweight pattern minimizes memory usage by
sharing common parts of objects across multiple
instances. In this example, the Flyweight class
defines the interface for flyweight objects.
ConcreteFlyweight implements the shared functionality.
FlyweightFactory manages flyweight objects and
ensures they are shared. The client code demonstrates
how flyweights are retrieved from the factory
and used with extrinsic state."""


class Flyweight[T]:
    def operation(self, extrinsic_state: str) -> T:
        raise NotImplementedError


class ConcreteFlyweight(Flyweight[str]):
    def operation(self, extrinsic_state: str):
        return f"ConcreteFlyweight operation with {extrinsic_state}"


class FlyweightFactory:
    def __init__(self):
        self.flyweights: dict[str, Flyweight[str]] = {}

    def get_flyweight(self, key: str):
        if key not in self.flyweights:
            self.flyweights[key] = ConcreteFlyweight()
        return self.flyweights[key]


# Client code
factory = FlyweightFactory()
flyweight1 = factory.get_flyweight("key1")
flyweight2 = factory.get_flyweight("key2")

result1 = flyweight1.operation("state1")
result2 = flyweight2.operation("state2")

print("Flyweight 1 result:", result1)
print("Flyweight 2 result:", result2)
