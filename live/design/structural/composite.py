"""
COMPOSITE DESIGN PATTERN
========================
The Composite pattern composes objects
into tree structures to represent part-whole
hierarchies. In this example, the Component
class defines the interface for leaf and
composite objects. The Leaf class represents
individual objects, and the Composite class
represents compositions of objects. The
client code demonstrates how leaf and
composite objects can be combined in a
hierarchical structure, allowing uniform
treatment of individual and composed objects."""


class Component:
    def operation(self):
        pass


class Leaf(Component):
    def operation(self):
        return "Leaf operation"


class Composite(Component):
    def __init__(self):
        self.children = []

    def add(self, component):
        self.children.append(component)

    def remove(self, component):
        self.children.remove(component)

    def operation(self):
        results = [child.operation() for child in self.children]
        return f'Composite operation: {", ".join(results)}'


# Client code
leaf1 = Leaf()
leaf2 = Leaf()
composite = Composite()
composite.add(leaf1)
composite.add(leaf2)

result_leaf1 = leaf1.operation()
result_leaf2 = leaf2.operation()
result_composite = composite.operation()

print("Leaf 1 result:", result_leaf1)
print("Leaf 2 result:", result_leaf2)
print("Composite result:", result_composite)
