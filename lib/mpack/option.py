import typing as ty
from typing import Any

__all__ = "Option", "NONE", "NONETYPE"


def _scrub_class(Class: ty.Type, val=None):
    Class.__new__ = lambda *_, **__: val
    Class.__init__ = lambda *_, **__: None
    if not hasattr(Class, "__eq__"):
        Class.__eq__ = lambda s, o: s is o


def _single_none(Class: ty.Type):
    instance = None

    def get_instance(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = Class(*args, **kwargs)
            _scrub_class(Class, instance)
        return instance

    return get_instance


@_single_none
class _NONETYPE:
    def __str__(self) -> str:
        return "<NONE>"

    def __bool__(self) -> bool:
        return False

    def __setattr__(self, _: str, __: Any) -> None:
        raise NotImplementedError

    def __delattr__(self, _: str) -> None:
        raise NotImplementedError

    def __getattribute__(self, _: str) -> Any:
        raise NotImplementedError

    def __init_subclass__(cls) -> None:
        raise NotImplementedError

    __repr__ = __str__


NONE: _NONETYPE = _NONETYPE()
NONETYPE: ty.Type = type(NONE)
_T = ty.TypeVar("_T")
_Optional: ty.TypeAlias = ty.Union[_T, _NONETYPE]


class Option(ty.Generic[_T]):
    def __init__(self, value: _Optional[_T] = NONE) -> None:
        self._val: _Optional[_T] = value

    def has_value(self) -> bool:
        return self._val is not NONE

    def __bool__(self) -> bool:
        return self.has_value()

    def value(self) -> _T:
        "This function may throw[ValueError] if it holds a None."
        if self.has_value():
            return self._val
        raise ValueError("Empty Option")

    def value_or(self, value: _T) -> _T:
        return self._val if self.has_value() else value

    def transform(self, func: ty.Callable[[_T], _Optional[_T]]) -> ty.Self:
        return (
            self.__class__(func(self._val))
            if self.has_value()
            else self.__class__(self._val)
        )

    def or_else(self, func: ty.Callable[[], ty.Any]) -> ty.Self:
        if not self.has_value():
            func()
        return self

    def and_then(self, func: ty.Callable[[_T], ty.Any]) -> ty.Self:
        if self.has_value():
            func(self._val)
        return self

    def reset(self, value: _Optional[_T] = NONE) -> ty.Self:
        self._val = value
        return self

    def __str__(self) -> str:
        return f"Option(value={self._val!r})"

    __repr__ = __str__
