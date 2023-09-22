from typing import Any, Callable, Generic, Protocol, Type, TypeVar

from mpack import print

T = TypeVar("T")


def call_with(**kwargs: Any):
    def called(func: Callable[..., Any]):
        def new_args(**nkwargs: Any):
            return func(**{**kwargs, **nkwargs})

        return new_args

    return called


class class_decorator:
    def __init__(self, func: Callable[..., Any]) -> None:
        self.function = func

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.function(*args, **kwds)

    def another_one(self):
        print("Another ONE")


class _call_with_helper:
    def __init__(self, store, function: Callable[..., Any]) -> None:
        self.function = function
        self._store = store

    def __call__(self, **kwds: Any) -> Any:
        return self.function(**{**self._store.kwargs, **kwds})


class class_call_with:
    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs
        self.functions = []

    def decorate(self, function: Callable[..., Any]):
        func = _call_with_helper(self, function)
        self.functions.append(func)
        return func

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return [func(*args, **kwds) for func in self.functions]


class Singleton(Generic[T]):
    def __init__(self, cls: Type[T]) -> None:
        self.warpped_class: Type[T] = cls
        self.class_name = cls.__name__
        self.instance: T | None = None
        print(f"Making {self.class_name!r} a Singleton Class")

    def __call__(self, *args: Any, **kwds: Any) -> T:
        if self.instance is not None:
            print(f"Instance Already created for {self.class_name!r}")
            return self.instance
        print(f"Creating new instance for {self.class_name!r}")
        instance: T = self.warpped_class(*args, **kwds)
        self.instance = instance
        return instance
