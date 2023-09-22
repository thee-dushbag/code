from dataclasses import dataclass
from typing import (Any, Callable, Coroutine, Generic, Type, TypeVar, cast,
                    overload)

from .timable import Time

_T = TypeVar("_T")
FUNCTION_CALL_STR: str
TAKEN_TIME_STR: str
_Result = TimeitResult[_T]
_ResultCoro = Coroutine[None, None, _T]
_TimeitResultCoro = _ResultCoro[_Result[_T]]
_Function = Callable[..., _T]
_CoroFunction = _Function[_ResultCoro[_T]]
_TimeitFunction = _Function[_Result[_T]]
_TimeitFunctionCoro = _CoroFunction[_Result[_T]]
_TimeitConfFunction = Callable[[_Function[_T]], _Function[_Result[_T]]]
_TimeitConfFunctionCoro = Callable[[_CoroFunction[_T]], _CoroFunction[_Result[_T]]]

def get_config(*, call_str=None, time_str=None) -> TimeitConfig: ...

class TimeitFunction(Generic[_T]):
    func: _Function[_T] | _CoroFunction[_T]
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    def call(self) -> Any: ...
    async def acall(self) -> Any: ...
    def __str__(self) -> str: ...

class TimeitResult(Generic[_T]):
    lapse: Time
    result: _T
    target: TimeitFunction[_T]
    def __str__(self) -> str: ...

@dataclass
class TimeitConfig:
    function_call_str: str
    taken_time_str: str

def str_func_args_kwargs(*args: Any, **kwargs: dict[str, Any]) -> tuple[str, str]: ...
def timer_sync(
    func: _Function[_T], config: TimeitConfig | None = None
) -> _TimeitFunction[_T]: ...
def timer_async(
    func: _CoroFunction[_T], config: TimeitConfig | None = None
) -> _TimeitFunctionCoro[_T]: ...
@overload
def timer(
    func: _CoroFunction[_T], config: TimeitConfig | None = None
) -> _TimeitFunctionCoro[_T]: ...
@overload
def timer(
    func: _Function[_T], config: TimeitConfig | None = None
) -> _TimeitFunction[_T]: ...
def timer_sync_conf(config: TimeitConfig) -> _TimeitConfFunction[Any]: ...
def timer_async_conf(config: TimeitConfig) -> _TimeitConfFunctionCoro[Any]: ...
def timer_conf(config: TimeitConfig) -> _Function[Any]:
    "Please use timer_sync_conf or timer_async_conf for type hints."
