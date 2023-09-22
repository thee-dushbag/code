from typing import Any, Callable


class AdjacentOperate:
    def __new__(cls, data: list[Any], func: Callable[..., Any]) -> list[Any]:
        if not data:
            return []
        cls.func: Callable[..., Any] = func
        cls._cache = []
        cls.data = data
        cls._crush_until()  # type: ignore
        return cls._cache

    @classmethod
    def _crush_until(cls) -> None:
        while cls._stack_crusher():  # type: ignore
            cls.data: list[Any] = cls._cache

    @classmethod
    def _stack_crusher(cls) -> bool:
        crushed: bool = False
        cls._cache: list[Any] = [cls.data[0]]
        for value in cls.data[1:]:
            if cls._cache[-1] == value:
                cls._cache[-1] = cls.func(value)
                crushed = True
            else:
                cls._cache.append(value)
        return crushed
