"""
Instances all the way down.
"""

from typing import Any

NUMBER = 5052


class MetaClass(type):
    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        properties: dict[str, Any],
        *,
        number: int | None = None,  # intended to be passed to MetaClass.__init__
    ):
        return type.__new__(
            cls, name, bases, properties
        )  # After this, __init__ is called.

    def __init__(
        self,
        name: str,
        bases: tuple[type, ...],
        properties: dict[str, Any],
        *,
        number: int | None = None,
    ):
        self.class_number = NUMBER if number is None else number
        self.class_name = name
        self.superclasses = bases
        self.class_props = properties

    def square_number(self) -> int:
        return self.class_number**2

    @property
    def double_number(self) -> int:
        return self.class_number * 2

    def plus_one(self):
        self.class_number += 1


class ClassOne(metaclass=MetaClass, number=3):
    def __init__(self, name: str, value: int) -> None:
        self.instance_name = name
        self.instance_number = value

    @classmethod  # Try to keep MetaClass.square_number within reach
    def cls_square_number(cls):  # by aliasing it with a new access name
        return MetaClass.square_number(cls)

    def square_number(self) -> int:  # Hides ClassOne.square_number
        return self.instance_number**2

    @classmethod
    def plus_two(cls):
        cls.class_number += 2

    @property
    def double_number(self) -> int:
        return self.instance_number * 2


instance = ClassOne("instance", 4)
print(f"{instance.square_number() = }")
print(f"{instance.class_number = }")
print(f"{instance.instance_number = }")
instance.plus_two()
print(f"{instance.class_number = }")
ClassOne.plus_one()
print(f"{ClassOne.class_number = }")

try:
    # No longer a true class method but its instances method
    print(f"{ClassOne.square_number() = }")  # type: ignore
except TypeError as e:
    print(e)
finally:
    # An alias classmethod descriptor to the original square_number true class method
    print(f"{ClassOne.cls_square_number() = }")

try:
    # Cannot be found since it is a true class method
    # which is not in this instances lookup path
    print(f"{instance.plus_one() = }")  # type: ignore
except AttributeError as e:
    print("cannot access true class method from the class' instance: %r" % e.name)
finally:
    # Okay since it does exist in ClassOne.__dict__ as a method
    print(f"{instance.square_number() = }")

print(f'{ClassOne.class_props = }')
print(f"{ClassOne.class_name = }")
print(f"{instance.instance_name = }")
print(f"{instance.class_name = }")
print(f"{instance.class_number = }")
print(f"{instance.instance_number = }")
print(f"{instance.instance_number * ClassOne.class_number = }")
