"""This is a package containing all my python reusable code projects."""
from rich import print
from ._main import main, get_modname
from typing import Callable, Optional, TypeAlias, TypeVar, Type, Any

this = get_modname

__all__ = 'main', 'get_modname', 'convert', 'cast', 'print', 'this'

T = TypeVar('T')
Converter: TypeAlias = Callable[[Any], T]

def convert(type_: Type[T], value: Any, converter: Optional[Converter]=None) -> T:
    _con: Converter = converter or type_
    return _con(value)

def cast(_: Type[T], value) -> T:
    return value