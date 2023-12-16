from dataclasses import dataclass
import typing as ty
from .timable import Time

_T = ty.TypeVar("_T")
FUNCTION_CALL_STR: str
TAKEN_TIME_STR: str
_Result = TimeitResult[_T]
_ResultCoro = ty.Coroutine[None, None, _T]
_TimeitResultCoro = _ResultCoro[_Result[_T]]
_Function = ty.Callable[..., _T]
_CoroFunction = _Function[_ResultCoro[_T]]
_TimeitFunction = _Function[_Result[_T]]
_TimeitFunctionCoro = _CoroFunction[_Result[_T]]
_TimeitConfFunction = ty.Callable[[_Function[_T]], _Function[_Result[_T]]]
_TimeitConfFunctionCoro = ty.Callable[[_CoroFunction[_T]], _CoroFunction[_Result[_T]]]

def get_config(*, call_str=None, time_str=None) -> TimeitConfig: ...

class TimeitFunction(ty.Generic[_T]):
    func: _Function[_T] | _CoroFunction[_T]
    args: tuple[ty.Any, ...]
    kwargs: dict[str, ty.Any]
    def call(self) -> ty.Any: ...
    async def acall(self) -> ty.Any: ...
    def __str__(self) -> str: ...

class TimeitResult(ty.Generic[_T]):
    lapse: Time
    result: _T
    target: TimeitFunction[_T]
    def __str__(self) -> str: ...

@dataclass
class TimeitConfig:
    function_call_str: str
    taken_time_str: str

def str_func_args_kwargs(
    *args: ty.Any, **kwargs: dict[str, ty.Any]
) -> tuple[str, str]: ...
def timer_sync(
    func: _Function[_T], config: TimeitConfig | None = None
) -> _TimeitFunction[_T]: ...
def timer_async(
    func: _CoroFunction[_T], config: TimeitConfig | None = None
) -> _TimeitFunctionCoro[_T]: ...
@ty.overload
def timer(
    func: _CoroFunction[_T], config: TimeitConfig | None = None
) -> _TimeitFunctionCoro[_T]: ...
@ty.overload
def timer(
    func: _Function[_T], config: TimeitConfig | None = None
) -> _TimeitFunction[_T]: ...
def timer_sync_conf(config: TimeitConfig) -> _TimeitConfFunction[ty.Any]: ...
def timer_async_conf(config: TimeitConfig) -> _TimeitConfFunctionCoro[ty.Any]: ...
def timer_conf(config: TimeitConfig) -> _Function[ty.Any]:
    "Please use timer_sync_conf or timer_async_conf for type hints."
