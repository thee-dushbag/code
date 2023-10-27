"""
Module exports a terminal command that can be used a below.
Example:
    >>> ls
    app.py
    
    >>> cat app.py
    from aiohttp import web
    routes = web.RouteTableDef()
    
    @routes.get('/')
    async def index(request: web.Request):
        return web.Response(text='Hello World')
    
    async def app_factory():
        app = web.Application()
        app.add_routes(routes)
        return app
    
    >>> webrun app:app_factory --bind localhost:9080
    Serving on http://localhost:9080.
    (Press Ctrl-C to exit)
    ...
"""

from dataclasses import dataclass
from importlib import import_module
from types import ModuleType
from typing import Callable, Coroutine

import click
from aiohttp import web
from click.core import Context, Parameter
from uvloop import install as install_uvloop


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
        return self.__doc__ or ""

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
        if not factory:
            factory = "application"
        module, _, package = module.partition(".")
        module = import_module(module, package=package or None)
        factory = getattr(module, factory)
        return TargetArg(module, factory)


@click.command
@click.option(
    "--bind",
    "-b",
    type=BindParam(),
    help=BindParam.__doc__,
    default=BindArg("localhost", 8080),
)
@click.argument("target", type=TargetParam())
@click.help_option('--help', '-h')
def main(bind: BindArg, target: TargetArg):
    """Serve an aiohttp application {TARGET} <[package.]module>:<app_factory> on {BIND} <host>:<port>"""
    try:
        install_uvloop()
        web.run_app(target.target(), host=bind.host, port=bind.port)
    except KeyboardInterrupt:
        ...
    except Exception as e:
        click.echo(str(e), err=True)


if __name__ == "__main__":
    main()
