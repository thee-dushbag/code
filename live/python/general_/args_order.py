from typing import Callable, TypeVar


T = TypeVar("T")


def param(name: str, value: T) -> Callable[[], T]:
    def get_value() -> T:
        print("Read Param: %s: %r" % (name, value))
        return value

    return get_value


def add(a, b, c):
    return a + b + c

a = param('a', 1)
b = param('b', 2)
c = param('c', 3)

print(add(a(), b(), c()))
