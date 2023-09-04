from dataclasses import dataclass
from importlib import import_module
from types import ModuleType
from typing import Callable, Coroutine
from click.core import Context, Parameter
from aiohttp import web
from uvloop import install as install_uvloop
import click


@dataclass
class BindArg:
    host: str
    port: int


@dataclass
class TargetArg:
    module: ModuleType
    target: Callable[[], Coroutine[None, None, web.Application]]


class BindParam(click.ParamType):
    "String of format '<host:str>:<port:int>'."
    name = "BindParam"

    def convert(
        self, value: str, param: Parameter | None, ctx: Context | None
    ) -> BindArg:
        def fail(message: str):
            self.fail(message, param, ctx)

        if ":" not in value or not value.count(":") == 1:
            fail(
                f"Invalid Bind argumant: expected <host:str>:<port:int>, found {value!r}"
            )
        host, sport, *_ = value.split(":")
        if not sport.isnumeric():
            fail(f"Expected the port to be an integer: found {sport!r}")
        if not host:
            host = "localhost"
        port = int(sport)
        return BindArg(host, port)


class TargetParam(click.ParamType):
    "String of format '<module:ModuleType>:<factory:Awaitable[web.Application]>'."
    name = "TargetParam"

    @property
    def help(self) -> str:
        return self.__doc__ or ''

    def convert(
        self, value: str, param: Parameter | None, ctx: Context | None
    ) -> TargetArg:
        if value.count(":") > 1:
            self.fail(
                f"Invalid target arg: expected module:factory, found {value!r}",
                param,
                ctx,
            )
        if ":" not in value:
            module, factory = value, "application"
        module, _, factory, *_ = value.partition(":")
        if not factory: factory = 'application'
        module, _, package = module.partition(".")
        module = import_module(module, package=package or None)
        factory = getattr(module, factory)
        return TargetArg(module, factory)


@click.command
@click.option("--bind", "-b", type=BindParam(), help=BindParam.__doc__)
@click.argument("target", type=TargetParam())
def main(bind: BindArg, target: TargetArg):
    try:
        install_uvloop()
        if bind is None: bind = BindArg('localhost', 8080)
        web.run_app(target.target(), host=bind.host, port=bind.port)
    except KeyboardInterrupt:
        ...

if __name__ == '__main__':
    main()