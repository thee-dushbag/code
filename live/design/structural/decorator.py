"""
DECORATOR DESIGN PATTERN
========================
The Decorator pattern attaches additional
responsibilities to objects dynamically. In
this example, the Component class defines the
base interface, and the ConcreteComponent
class provides the basic implementation.
The Decorator class has a reference to a
Component and maintains a 'has-a' relationship.
ConcreteDecorator classes add or modify
behavior. The client code demonstrates
how decorators can be stacked to add
multiple layers of functionality to objects."""


class Component[T]:
    def operation(self) -> T:
        raise NotImplementedError


class ConcreteComponent(Component):
    def operation(self):
        return "ConcreteComponent operation"


class Decorator(Component):
    def __init__(self, component):
        self.component = component

    def operation(self):
        return self.component.operation()


class ConcreteDecoratorA(Decorator):
    def operation(self):
        return f"ConcreteDecoratorA operation + {self.component.operation()}"


class ConcreteDecoratorB(Decorator):
    def operation(self):
        return f"ConcreteDecoratorB operation + {self.component.operation()}"


# Client code
component = ConcreteComponent()
decorator_a = ConcreteDecoratorA(component)
decorator_b = ConcreteDecoratorB(decorator_a)

result_component = component.operation()
result_decorator_a = decorator_a.operation()
result_decorator_b = decorator_b.operation()

print("Component result:", result_component)
print("Decorator A result:", result_decorator_a)
print("Decorator B result:", result_decorator_b)
