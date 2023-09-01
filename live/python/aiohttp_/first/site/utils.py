from typing import Any, TypeVar, Type

T = TypeVar('T')

class MISSING:
    ...

sentinel = MISSING()

def is_missing(__attr: Any) -> bool:
    return isinstance(__attr, MISSING)

def missing_or(__type: Type[T], value: Any) -> T | MISSING:
    return value if is_missing(value) else __type(value)

