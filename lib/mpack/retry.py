import functools
import typing
import time

P = typing.ParamSpec("P")
T = typing.TypeVar("T")


class RetryError(typing.Generic[P, T], Exception):
    def __init__(
        self,
        function: typing.Callable[P, T],
        errors: typing.Sequence[Exception],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        self.args = args
        self.kwargs = kwargs
        self.function = function
        self.errors = errors

    def link_causes(self):
        error = self
        for e in self.errors:
            error.__cause__ = e
            error = e
        return self


@typing.overload
def retry(
    *,
    on: typing.Sequence[type[Exception]] | None = ...,
    count: int | None = ...,
    delay: float | None = ...,
) -> typing.Callable[[typing.Callable[P, T]], typing.Callable[P, T]]: ...


@typing.overload
def retry(
    func: typing.Callable[P, T],
    /,
    *,
    on: typing.Sequence[type[Exception]] | None = ...,
    count: int | None = ...,
    delay: float | None = ...,
) -> typing.Callable[P, T]: ...


def retry(
    func=None,
    /,
    *,
    on=None,
    count=None,
    delay=None,
):
    count = 3 if count is None else count
    delay = 0 if delay is None else delay
    on = (Exception,) if on is None else on

    def _retry_impl(func: typing.Callable[P, T], /) -> typing.Callable[P, T]:
        @functools.wraps(func)
        def get_args(*args: P.args, **kwargs: P.kwargs):
            errors = []
            for _ in range(count):
                try:
                    return func(*args, **kwargs)
                except on as e:
                    errors.append(e)
                time.sleep(delay)
            raise RetryError(func, errors, *args, **kwargs)

        return get_args

    return _retry_impl if func is None else _retry_impl(func)
