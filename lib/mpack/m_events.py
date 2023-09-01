from concurrent.futures import ThreadPoolExecutor, wait
from typing_extensions import Self
from typing import Any, Callable, Union
from functools import wraps

__all__: tuple[str, ...] = ("Event","EventObject", "EventTask")

class EventObject:
    def __init__(self, event: str, data: Any = None) -> None:
        self.event = str(event)
        self.data = data

    @staticmethod
    def construct(obj):
        return obj if isinstance(obj, EventObject) else EventObject(str(obj))

    def __eq__(self: Self, __value: Union['EventObject', Any]) -> bool:
        __value = EventObject.construct(__value)
        return self.event == __value.event

    def __str__(self) -> str:
        return f"EventObject(event='{self.event}', data={self.data})"

    def __hash__(self) -> int:
        return hash(self.event)

class EventTask:
    def __init__(
        self: Self, func: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> None:
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.last = None

    @classmethod
    def construct(cls, func: Callable[..., Any] | 'EventTask', *args: Any, **kwargs) -> 'EventTask':
        return func if isinstance(func, EventTask) else EventTask(func, *args, **kwargs)

    def __call__(self: Self, event_object: EventObject) -> Any:
        self.last = self.func(event_object, *self.args, **self.kwargs)
        return self.last

    def __eq__(self: Self, func: "EventTask") -> bool:
        return self.func.__code__ == func.func.__code__


class Event:
    _executor = ThreadPoolExecutor(thread_name_prefix="EventGroupThread_")

    def __init__(self: Self, **mappings: list[EventTask]) -> None:
        self._event_rg: dict[EventObject | str, list[EventTask]] = {
            EventObject.construct(key): value for key, value in mappings.items()
        }

    def emit(self: Self, event: EventObject | str) -> None:
        event = EventObject.construct(event)
        if targets := self._event_rg.get(event):
            wait([self._executor.submit(target, event) for target in targets])

    def listen(
        self: Self,
        event: EventObject | str,
        func: Callable[..., Any] | EventTask,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        obj = EventTask.construct(func, *args, **kwargs)
        if not event in self._event_rg:
            self._event_rg[event] = []
        self._event_rg[event].append(obj)

    def unsub(self: Self, event: EventObject | str, func: Callable[..., Any]) -> None:
        event = EventObject.construct(event)
        if suspects := self._event_rg.get(event):
            target: EventTask = EventTask(func)
            self._event_rg[event] = [okay for okay in suspects if okay != target]

    def drop(self: Self, event: EventObject | str) -> None:
        if event in self._event_rg:
            self._event_rg.pop(event)

def eventable(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def inner(event_object: EventObject, *args: Any, **kwargs: Any) -> Any:
        inner.event_object = event_object # type: ignore
        res = func(*args, **kwargs)
        return res
    return inner