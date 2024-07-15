"""
FACADE DESIGN PATTERN
=====================
The Facade pattern provides a simplified
interface to a complex subsystem. In this
example, the Subsystem classes have their
own interfaces, and the Facade class provides
a higher-level interface that coordinates
their interactions. The client code
demonstrates how the Facade hides the
complexity of the subsystem and provides
a unified way to access its functionality."""


class SubsystemA:
    def operation_a(self):
        return "SubsystemA operation"


class SubsystemB:
    def operation_b(self):
        return "SubsystemB operation"


class SubsystemC:
    def operation_c(self):
        return "SubsystemC operation"


class Facade:
    def __init__(self):
        self.subsystem_a = SubsystemA()
        self.subsystem_b = SubsystemB()
        self.subsystem_c = SubsystemC()

    def operation(self):
        results = (
            self.subsystem_a.operation_a(),
            self.subsystem_b.operation_b(),
            self.subsystem_c.operation_c(),
        )
        return f'Facade operation: {", ".join(results)}'


# Client code
facade = Facade()
result = facade.operation()

print("Facade result:", result)
