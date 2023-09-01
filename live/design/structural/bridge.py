"""
THE BRIDGE DESIGN PATTERN
=========================
The Bridge pattern separates an abstraction
from its implementation, allowing both to vary
independently. In this example, the Implementor
defines the interface for concrete implementations.
The Abstraction class uses an instance of
Implementor to perform its operation. The Refined
Abstraction class extends Abstraction and can
provide additional functionality. The client
code demonstrates how different implementations
can be combined with abstractions to create
various behavior combinations."""


from abc import ABC, abstractmethod


class Implementor(ABC):
    @abstractmethod
    def operation_implementation(self) -> str:
        pass


class ConcreteImplementorA(Implementor):
    def operation_implementation(self):
        return "ConcreteImplementorA operation"


class ConcreteImplementorB(Implementor):
    def operation_implementation(self):
        return "ConcreteImplementorB operation"


class Abstraction:
    def __init__(self, implementor: Implementor):
        self.implementor = implementor

    def operation(self):
        return self.implementor.operation_implementation()


class RefinedAbstraction(Abstraction):
    def operation(self):
        return f"RefinedAbstraction: {self.implementor.operation_implementation()}"


# Client code
implementor_a = ConcreteImplementorA()
implementor_b = ConcreteImplementorB()

abstraction_a = Abstraction(implementor_a)
abstraction_b = RefinedAbstraction(implementor_b)

result_a = abstraction_a.operation()
result_b = abstraction_b.operation()

print("Abstraction A result:", result_a)
print("Abstraction B result:", result_b)
