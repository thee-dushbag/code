from typing import Any, Callable, TypeVar, Generic, Optional
from concurrent.futures import ThreadPoolExecutor, wait
from attrs import define, field
from itertools import count
from threading import Lock


def _create_key_keeper():
    _keeper = count()

    def _create_key():
        return str(next(_keeper))

    return _create_key


_create_hook_key = _create_key_keeper()
_create_depender_key = _create_key_keeper()

T = TypeVar("T")
K = TypeVar("K")
DependerCallback = Callable[["HookState[Any]"], Any]
DependerErrorback = Callable[["HookState[Any]", Exception], Any]

DEFAULT_CALLBACK = lambda *a, **k: None

_GLOBAL_STATE_MANAGER: Optional["HookStateManager"] = None


class HookMap(dict[str, "Hook[T]"]):
    ...


class DependerMap(dict[str, "Depender[T]"]):
    ...


def get_manager():
    global _GLOBAL_STATE_MANAGER
    if _GLOBAL_STATE_MANAGER is None:
        _GLOBAL_STATE_MANAGER = HookStateManager()
    return _GLOBAL_STATE_MANAGER  # type:ignore


@define
class HookStateManager:
    _hooks: HookMap = field(factory=HookMap, init=False)
    _runner: ThreadPoolExecutor = field(factory=ThreadPoolExecutor)

    def create_hook(self, value: K) -> "Hook[K]":
        hook = Hook(value, self)
        self._hooks[hook._key] = hook
        return hook

    def destroy(self, hook: "Hook"):
        if self.get_hook(hook._key):
            del self._hooks[hook._key]
        hook._kill()

    def get_hook(self, hook_key: str):
        return self._hooks.get(hook_key, None)

    def __call__(self, value: T) -> "Hook[T]":
        return self.create_hook(value)


@define
class _ImplHookState(Generic[T]):
    _hook: "Hook[T]"

    def kill(self):
        self._hook.kill()

    def with_depender(self, callback: DependerCallback | "Depender[T]", errorback=None):
        depender = (
            callback
            if isinstance(callback, Depender)
            else Depender(callback, errorback or DEFAULT_CALLBACK)
        )
        depender.listen_to(self)
        return depender


@define
class FrozenHookState(_ImplHookState[T]):
    def get_value(self) -> T:
        return self._hook._get_value()

    def with_getter(self, function: Callable[..., T]):
        def _called(*args: Any, **kwargs: Any) -> T:
            value = self.get_value()
            return function(value, *args, **kwargs)

        return _called


@define
class BlindHookState(_ImplHookState[T]):
    def set_value(self, value: T):
        self._hook._set_value(value)

    def with_setter(self, function: Callable[..., T]):
        def _called(*args: Any, **kwargs: Any) -> T:
            value = function(*args, **kwargs)
            self.set_value(value)
            return value

        return _called


@define
class HookState(BlindHookState[T], FrozenHookState[T]):
    def with_setget(
        self, setter: Callable[..., T], getter: Callable[..., T] | None = None
    ) -> tuple[Callable[..., None], Callable[..., T]]:
        def _called(*args: Any, **kwargs: Any):
            self.set_value(setter(*args, **kwargs))

        return (
            _called,
            (lambda *a, **k: getter(self.get_value(), *a, **k))
            if getter
            else self.get_value,
        )


@define
class Hook(Generic[T]):
    _state: T
    _manager: HookStateManager = field(factory=get_manager)
    dependents: DependerMap = field(factory=DependerMap, init=False)
    _key: str = field(init=False, factory=_create_hook_key)
    _alive: bool = field(init=False, default=True)
    _lock: Lock = field(init=False, factory=Lock)

    def depend(self, depender: "Depender[T]"):
        self.dependents[depender._key] = depender

    def forget(self, depender: "Depender[T]"):
        if depender._key in self.dependents:
            del self.dependents[depender._key]

    def _update_state(self, value: T):
        with self._lock:
            self._state = value

    def _set_value(self, value: T):
        if not self._alive:
            return
        self._update_state(value)
        self._notify_dependents()

    def _kill(self):
        print(f"Killing: Hook with state: {self._state!r}")
        self._alive = False
        self._update_state(None)  # type:ignore

    def kill(self):
        self._manager.destroy(self)

    def _notify_dependents(self):
        hook_state = HookState(self)

        def _notify(depender: "Depender[T]"):
            depender.notify(hook_state)

        wait(self._manager._runner.submit(_notify, d) for d in self.dependents.values())

    def _get_value(self):
        return self._state

    def create_state(self) -> HookState[T]:
        return HookState(self)


@define
class Depender(Generic[T]):
    callback: DependerCallback
    errorback: DependerErrorback = field(default=DEFAULT_CALLBACK)
    active: bool = field(default=True, kw_only=True)
    _key: str = field(init=False, factory=_create_depender_key)

    def _use_value(self, hook_state: HookState[T]):
        if not self.active:
            return
        try:
            self.callback(hook_state)
        except Exception as e:
            self.errorback(hook_state, e)

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    @property
    def is_active(self) -> bool:
        return self.active

    def notify(self, hook_state: HookState[T]):
        self._use_value(hook_state)

    def __call__(self, hook_state: HookState[T]):
        self._use_value(hook_state)

    def listen_to(self, hook_state: _ImplHookState[T]):
        hook_state._hook.depend(self)

    def forget(self, hook_state: _ImplHookState[T]):
        hook_state._hook.forget(self)

    def with_callback(self, function: DependerCallback):
        self.callback = function

    def with_errorback(self, function: DependerErrorback):
        self.errorback = function


def state(value: T) -> HookState[T]:
    return HookState(Hook(value))


def frozen_state(value: T) -> FrozenHookState[T]:
    return FrozenHookState(Hook(value))


def blind_state(value: T) -> BlindHookState[T]:
    return BlindHookState(Hook(value))


def make_blind(state: _ImplHookState[T]) -> BlindHookState[T]:
    return BlindHookState(state._hook)


def make_frozen(state: _ImplHookState[T]) -> FrozenHookState[T]:
    return FrozenHookState(state._hook)


def make_state(state: _ImplHookState[T]) -> HookState[T]:
    return HookState(state._hook)


def depend_on(
    hook_state: HookState,
    callback: DependerCallback,
    errorback: Optional[DependerErrorback] = None,
):
    return hook_state.with_depender(callback, errorback)


def consume_state(func: Callable[..., Any]):
    def _consumer(state: FrozenHookState[T]) -> T | None:
        return func(state.get_value())

    return _consumer
