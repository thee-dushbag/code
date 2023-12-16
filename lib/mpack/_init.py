from rich import print
from ._main import get_modname, main
import typing as ty

this = get_modname

__all__ = "main", "get_modname", "convert", "cast", "print", "this"

T = ty.TypeVar("T")
Converter: ty.TypeAlias = ty.Callable[[ty.Any], T]


def convert(type_: ty.Type[T], value: ty.Any, converter: ty.Optional[Converter] = None) -> T:
    _con: Converter = converter or type_
    return _con(value)


def cast(_: ty.Type[T], value) -> T:
    return value