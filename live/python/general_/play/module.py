import sys
from types import ModuleType
from typing import Any, NoReturn
from mpack.timer import str_func_args_kwargs

def len(*_, **__): 'My Len Req Function'

def hello(name: str) -> NoReturn:
    print(f"Hello {name}, how was your day?")

class CallableModule(ModuleType):
    def __init__(self, name: str, doc: str | None = ...) -> None:
        super().__init__(name, doc)
        print(f"Initializing Module: {name=!r} {doc=!r}")
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        print(f"Setting attribute: {__name}={__value!r}")
        super().__setattr__(__name, __value)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        arg, k = str_func_args_kwargs(*args, **kwds)
        kwarg = f', {k}' if k and arg else k
        sargs = f'({arg}{kwarg})'
        print(f"Calling a Module with: {sargs}")
    
    def hola(self):
        print(f"Hola Mother fucker: {self}")


sys.modules[__name__].__class__ = CallableModule
