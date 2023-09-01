from itertools import zip_longest
from typing import (
    Generic,
    Protocol,
    MutableSequence,
    TypeVar,
    Callable,
    Iterator,
    Iterable
)


class LessThan(Protocol):
    def __le__(self, __o) -> bool:
        ...

class GreaterThan(Protocol):
    def __ge__(self, __o) -> bool:
        ...

T = TypeVar("T", LessThan, GreaterThan)

class streamer(Generic[T]):
    class target:
        def __init__(self, store: Iterable[T]) -> None:
            self.store = iter(store)
            self.value = None
            self.done = False
            self.use()
        def use(self) -> T | None:
            value = self.value
            try: self.value = next(self.store)
            except StopIteration:
                self.value = None
                self.done = True
            return value

    def __init__(self, selector: Callable[[T, T], bool], main_iter: Iterable[T], extra_iter: Iterable[T]) -> None:
        self.cache_main = streamer.target(main_iter)
        self.cache_extra = streamer.target(extra_iter)
        self.selector = selector
        self.done = False
    
    def __iter__(self) -> Iterator[T]:
        return self
    
    def __next__(self) -> T:#type:ignore
        if self.cache_extra.done and self.cache_main.done:
            raise StopIteration
        if self.cache_extra.done:
            return self.cache_main.use() #type:ignore
        if self.cache_main.done:
            return self.cache_extra.use()#type:ignore
        if self.selector(self.cache_extra.value, self.cache_main.value): #type: ignore
            return self.cache_extra.use() #type:ignore
        else:
            return self.cache_main.use() #type:ignore


class mergesort(Generic[T]):
    def __new__(cls, container, reverse: bool = False) -> MutableSequence[T]:
        cls.compare = cls.descending if reverse else cls.ascending
        if len(container) <= 1:
            return container
        powder: MutableSequence[list[T]] = cls.powderfy(container)
        while len(powder) != 1:
            powder = cls.sort(powder)
        return powder[0]

    @classmethod
    def sort(cls, powder: MutableSequence[list[T]]) -> MutableSequence[list[T]]:
        piter = iter(powder)
        return [
            list(streamer(cls.compare, one, two)) if one and two else one or two
            for one, two in zip_longest(piter, piter)
        ]

    @classmethod
    def ascending(cls, one: T, two: T) -> bool:
        return one <= two

    @classmethod
    def descending(cls, one: T, two: T) -> bool:
        return one >= two

    @classmethod
    def powderfy(cls, container: MutableSequence[T]) -> list[list[T]]:
        return [[x] for x in container]
