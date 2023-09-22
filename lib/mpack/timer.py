from dataclasses import dataclass, field
from functools import partial
from functools import wraps as _wraps
from inspect import iscoroutinefunction
from time import perf_counter as _perf_counter
from typing import Any, Callable, TypeVar

from .timable import Time

FUNCTION_CALL_STR = "[{function_name}({args}, {kwargs})]"
TAKEN_TIME_STR = "{target}: Took {lapse._time} seconds."


def get_config(*, call_str=None, time_str=None):
    func_call_str = call_str or FUNCTION_CALL_STR
    take_time_str = time_str or TAKEN_TIME_STR
    return TimeitConfig(function_call_str=func_call_str, taken_time_str=take_time_str)


T = TypeVar("T")


def str_func_args_kwargs(*args: Any, **kwargs: dict[str, Any]) -> tuple[str, str]:
    args_str = ", ".join(f"{arg!r}" for arg in args)
    kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
    return args_str, kwargs_str


@dataclass(kw_only=True, frozen=True, slots=True)
class TimeitConfig:
    function_call_str: str = field()
    taken_time_str: str = field()


@dataclass(frozen=True, slots=True)
class TimeitFunction:
    config: TimeitConfig
    func: Callable[..., Any]
    args: tuple[Any, ...] = field(default_factory=tuple)
    kwargs: dict[str, Any] = field(default_factory=dict)

    def sync_call(self) -> Any:
        return self.func(*self.args, **self.kwargs)

    async def async_call(self) -> Any:
        return await self.func(*self.args, **self.kwargs)

    def __call__(self):
        return self.sync_call()

    def __str__(self) -> str:
        args, kwargs = str_func_args_kwargs(*self.args, **self.kwargs)
        fname = self.func.__name__
        return self.config.function_call_str.format(
            function_name=fname, args=args, kwargs=kwargs
        )


@dataclass(frozen=True, slots=True)
class TimeitResult:
    config: TimeitConfig
    lapse: Time
    result: Any
    target: TimeitFunction

    def __str__(self) -> str:
        return self.config.taken_time_str.format(lapse=self.lapse, target=self.target)


def timer_sync(func, config: TimeitConfig | None = None):
    config = config or get_config()

    @_wraps(func)
    def _timeit(*args, **kwargs) -> TimeitResult:
        timeitfunc = TimeitFunction(config, func, args, kwargs)
        start = _perf_counter()
        result = timeitfunc.sync_call()
        lapse = Time(_perf_counter() - start)
        return TimeitResult(config, lapse, result, timeitfunc)

    return _timeit


def timer_async(func: Callable[..., Any], config: TimeitConfig | None = None):
    config = config or get_config()

    @_wraps(func)
    async def _timeit(*args, **kwargs) -> TimeitResult:
        timeitfunc = TimeitFunction(config, func, args, kwargs)
        start = _perf_counter()
        result = await timeitfunc.async_call()
        lapse = Time(_perf_counter() - start)
        return TimeitResult(config, lapse, result, timeitfunc)

    return _timeit


def timer_sync_conf(config: TimeitConfig):
    return partial(timer_sync, config=config)


def timer_async_conf(config: TimeitConfig):
    return partial(timer_async, config=config)


def timer(func, config: TimeitConfig | None = None):
    return (
        timer_async(func, config)
        if iscoroutinefunction(func)
        else timer_sync(func, config)
    )


def timer_conf(config: TimeitConfig):
    return partial(timer, config=config)
