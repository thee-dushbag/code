import typing as ty

T = ty.TypeVar("T")

class Option(ty.Generic[T]):
    def __init__(self, value: ty.Optional[T] = None) -> None:
        self._val: ty.Optional[T] = value

    def has_value(self) -> bool:
        return self._val is not None

    def __bool__(self) -> bool:
        return self.has_value()

    def value(self) -> T:
        "This function may throw[ValueError] if it holds a None."
        if self.has_value(): return self._val
        raise ValueError("Empty Option")

    def value_or(self, value: T) -> T:
        return self._val if self.has_value() else value

    def transform(self, func: ty.Callable[[ty.Optional[T]], ty.Optional[T]]) -> ty.Self:
        return self.__class__(func(self._val))

    def or_else(self, func: ty.Callable[[], ty.Any]) -> ty.Self:
        if not self.has_value(): func()
        return self

    def and_then(self, func: ty.Callable[[T], ty.Any]) -> ty.Self:
        if self.has_value(): func(self._val)
        return self

    def __str__(self) -> str:
        return f"Option(value={self._val!r})"

    __repr__ = __str__
