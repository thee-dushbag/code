"""
THE SINGLETON DESIGN PATTERN
============================s
The Singleton pattern ensures that a class
has only one instance and provides a global
point of access to that instance. In this
example, the Singleton class uses a class
variable '_instance' to keep track of the
single instance created. The '__new__' method
ensures that only one instance is created and
returned. The client code demonstrates that
multiple attempts to create instances result
in the same single instance being returned."""


class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


# Client code
instance1 = Singleton()
instance2 = Singleton()

print("Are instance1 and instance2 the same object?", instance1 is instance2)
