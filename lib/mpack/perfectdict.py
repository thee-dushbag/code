import dataclasses as dt
import typing as ty

T = ty.TypeVar("T")


@dt.dataclass
class Values(ty.Generic[T]):
    old: T
    new: T


ValueTypeUpdater: ty.TypeAlias = ty.Callable[[Values[T]], T]


def DefaultUpdater(values: Values[T]) -> T:
    return values.new


class UpdaterBase:
    ...


class perfectdict(dict):
    ...
