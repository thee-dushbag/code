# Factory Method
# Defines an interface for creating objects but delegates the
# responsibility of which class to instantiate to its subclasses.

from abc import ABC, abstractmethod


# Abstract Product interface
class Product(ABC):
    @abstractmethod
    def operation(self) -> str:
        pass

    def operate(self):
        string: str = self.operation()
        print(f"Operating on: {string!r}")
    
    def __str__(self) -> str:
        string = self.operation()
        return f'{self.__class__.__name__}({string!r})'

# Concrete Products
class ConcreteProductA(Product):
    def operation(self):
        return "Product A"


class ConcreteProductB(Product):
    def operation(self):
        return "Product B"


# Creator (Factory Method)
class Creator(ABC):
    @abstractmethod
    def factory_method(self) -> Product:
        pass

    def operate(self):
        product = self.factory_method()
        self._operate(product)
    
    def _operate(self, product: Product):
        print(f"Created {product.__class__.__name__}")
        product.operate()


# Concrete Creators
class ConcreteCreatorA(Creator):
    def factory_method(self) -> Product:
        return ConcreteProductA()
    
    def operate(self):
        print("Aquiring resources...")
        product = self.factory_method()
        print(f"Established a connecting to: {product}")
        self._operate(product)

class ConcreteCreatorB(Creator):
    def factory_method(self) -> Product:
        return ConcreteProductB()


def main(creator: Creator):
    creator.operate()  # Output: Created Product A or Created Product B


if __name__ == "__main__":
    creator_a = ConcreteCreatorA()
    creator_b = ConcreteCreatorB()

    main(creator_a)  # Create Product A
    main(creator_b)  # Create Product B
