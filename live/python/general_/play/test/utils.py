from typing import Any, Callable, ParamSpec, TypeVar, cast

import bcrypt
import exc
from aiohttp.typedefs import Handler as _Handler
from aiohttp_mako import template

FORMAT = "utf-8"
_T = TypeVar("_T")


class Config(dict):
    def __init__(self, __config_key__: str, **kwds: Any):
        super().__init__(**kwds)
        self._config_key = __config_key__

    def __setattr__(self, __name: str, __value: Any) -> None:
        self[__name] = __value

    def __getattr__(self, __name: str, default: Any = exc._MISSING):
        if __name in self:
            return self[__name]
        if default is not exc._MISSING:
            return default
        raise exc.ConfigKeyNotFound(self._config_key, self)


P = ParamSpec("P")
_AKFunction = Callable[P, _T]
_Function = Callable[..., _T]
template = cast(_Function[_Function[_Handler]], template)


def hash_password(password: str) -> str:
    bpass = password.encode(FORMAT)
    salt = bcrypt.gensalt()
    hpass = bcrypt.hashpw(bpass, salt)
    return hpass.decode(FORMAT)


def check_password(password: str, hashed: str) -> bool:
    hpass = hashed.encode(FORMAT)
    bpass = password.encode(FORMAT)
    return bcrypt.checkpw(bpass, hpass)
