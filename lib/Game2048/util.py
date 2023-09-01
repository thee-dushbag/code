from typing import Any, Callable

class AdjacentOperate:
    def __new__(cls, data: list[Any], func: Callable[..., Any]) -> list[Any]:
        if not data:
            return []
        cls.func: Callable[..., Any] = func
        cls._cache = []
        cls.data = data
        cls.__crush_until(cls) # type: ignore
        return cls._cache

    def __crush_until(self) -> None:
        while self._stack_crusher(self): # type: ignore
            self.data: list[Any] = self._cache

    def _stack_crusher(self) -> bool:
        crushed: bool = False
        self._cache: list[Any] = [self.data[0]]
        for value in self.data[1:]:
            if self._cache[-1] == value:
                self._cache[-1] = self.func(value)
                crushed = True
            else:
                self._cache.append(value)
        return crushed
