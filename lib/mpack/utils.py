from functools import wraps
from typing import Any, Callable, Generic, Type, TypeVar

from . import print

T = TypeVar("T")


class Singleton(Generic[T]):
    def __init__(self, cls: Type[T]) -> None:
        self.warpped_class: Type[T] = cls
        self.instance: T | None = None

    def __call__(self, *args: Any, **kwds: Any) -> T:
        if self.instance is None:
            self.instance = self.warpped_class(*args, **kwds)
        return self.instance


def filter_keys(*, ok_keys=None, no_keys=None, overide_found=False, not_found=False):
    assert (
        any((ok_keys, no_keys)) or not_found
    ), "Must Pass ok_keys or no_keys as Iterable[str | Any]"
    not_found, overide_found = map(bool, (not_found, overide_found))
    ok_keys_i, no_keys_i = map(tuple, (ok_keys or (), no_keys or ()))

    def filterer(key: Any, *, o=None, no=None) -> bool:
        o, no = bool(o or overide_found), bool(no or not_found)
        ok_s, no_s = key in ok_keys_i, key in no_keys_i
        if not ok_s and not no_s:
            return no
        return not no_s if o else ok_s if ok_s and no_s else ok_s

    return filterer


class _MISSING:
    def __str__(self) -> str:
        return "<_MISSING_>"

    def __repr__(self) -> str:
        return self.__str__()

    def __call__(self, *_, **__):
        return self

    def __instancecheck__(self, _) -> bool:
        print(f"Checking: {_}")
        return False


MISSING = _MISSING()


class Deco:
    def __init__(self, value=None, attr_name=None, init=True) -> None:
        self._attr_name = str(attr_name)
        self.value = value
        self.init = init

    def _get_value(self, inst):
        if self._attr_name is None:
            return self.value
        return getattr(inst or self.cls, self._attr_name, MISSING)

    def _set_value(self, inst, value):
        if self._attr_name is None:
            self.value = value
        setattr(inst or self.cls, self._attr_name, value)

    def _raise_name_remap(self):
        assert (
            self.name != self._attr_name
        ), f"Property Remap Error: {self._name} is aliasing itself"

    def __set_name__(self, cls, name):
        self._name = f"{cls.__name__}.{name}"
        self.name, self.cls = name, cls
        self._raise_name_remap()
        if self.init:
            self._set_value(None, self.value)

    def __get__(self, inst, cls):
        value = self._get_value(inst)
        # print(f"Getting: {self._name} -> {value!r}")
        return value

    def __set__(self, inst, value):
        _value = self._get_value(inst)
        # print(f"Setting: {self._name}: {_value!r} -> {value!r}")
        self._set_value(inst, value)

    def __delete__(self, inst):
        # print(f"Deletting: {self._name} -> {self.value!r}")
        self._set_value(inst, MISSING)


def do_nothing(
    _F: Callable[..., Any] | None = None,
    *,
    return_value: Any = MISSING,
    call_with: Callable[..., Any] = MISSING,
):
    def _impl(*args, **kwargs):
        nonlocal return_value
        value = call_with(*args, **kwargs)
        if return_value is MISSING:
            return value
        return return_value

    if _F is None:
        return lambda func: wraps(func)(_impl)
    return wraps(_F)(_impl)


class Tracer:
    def __init__(self, function) -> None:
        self.calls = 0
        self.func = function

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.calls += 1
        print(
            f"Called {self.func.__name__} {self.calls} time{'s' if self.calls != 1 else ''}: [{args}, {kwargs}]"
        )
        return self.func(*args, **kwargs)

    def __get__(self, instance, owner):
        def _wrap(*a, **k):
            return self(instance, *a, **k)

        return _wrap
