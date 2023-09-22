"""This is a package containing all my python reusable code projects."""
from typing import Any, Callable, Optional, Type, TypeAlias, TypeVar

from rich import print

from ._main import get_modname, main

this = get_modname

__all__ = "main", "get_modname", "convert", "cast", "print", "this"

T = TypeVar("T")
Converter: TypeAlias = Callable[[Any], T]


def convert(type_: Type[T], value: Any, converter: Optional[Converter] = None) -> T:
    _con: Converter = converter or type_
    return _con(value)


def cast(_: Type[T], value) -> T:
    return value
