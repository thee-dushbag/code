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
from typing import Callable, Coroutine, TYPE_CHECKING, Never

if TYPE_CHECKING:
    from aiohttp import web
else:

    class web:
        Application = None


import click, re


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
    pattern = re.compile(
        r"(?P<host>[^:]+):(?P<port>\d+)",
        re.IGNORECASE,
    )

    def convert(
        self, value: str, param: click.Parameter | None, ctx: click.Context | None
    ) -> BindArg:
        match = re.fullmatch(self.pattern, value)
        if match is None:
            self.fail(f"Expected <host>:<port>, got {value!r}", param, ctx)

        host = match.group("host") or "0.0.0.0"
        port = match.group("port") or "8080"
        return BindArg(host, int(port))


class TargetParam(click.ParamType):
    "String of format '<module:ModuleType>:<factory:Awaitable[web.Application]>'."
    name = "TargetParam"
    pattern = re.compile(
        r"(?P<module>[^\s:]+)(:(?P<factory>[a-z0-9]+))?", re.IGNORECASE
    )

    @property
    def help(self) -> str:
        return self.__doc__ or ""

    def convert(
        self, value: str, param: click.Parameter | None, ctx: click.Context | None
    ) -> TargetArg:
        match = re.fullmatch(self.pattern, value)
        if match is None:
            self.fail(
                f"Expected target <module>:<factory>, got {value!r}",
                param,
                ctx,
            )

        modulename = match.group("module")
        factoryname = match.group("factory") or "application"

        if not modulename:
            self.fail(f"Invalid module name {modulename!r}", param, ctx)

        try:
            module = import_module(modulename)
        except ModuleNotFoundError as e:
            self.fail(repr(e), param, ctx)

        factory = getattr(module, factoryname, None)

        if factory is None:
            self.fail(
                "AttributeError: Cannot find Application instance "
                f"{factoryname!r} in module {module.__name__!r} at {module.__file__!r}",
                param,
                ctx,
            )
        return TargetArg(module, factory)


@click.command
@click.option("--uvloop/--no-uvloop", default=True)
@click.option(
    "--bind",
    "-b",
    type=BindParam(),
    help=BindParam.__doc__,
    default="localhost:8080",
)
@click.argument("target", type=TargetParam())
@click.help_option("--help", "-h")
def main(bind: BindArg, target: TargetArg, uvloop: bool):
    """Serve an aiohttp application {TARGET} <[package.]module>:<app_factory> on {BIND} <host>:<port>"""
    if uvloop:
        try:
            from uvloop import install as install_uvloop
        except ImportError:
            click.echo(
                "Failed intalling uvloop, import error, "
                "did you forget to install it?",
                err=True,
            )
        else:
            install_uvloop()

    try:
        from aiohttp import web

        web.run_app(target.target(), host=bind.host, port=bind.port)
    except ImportError:
        click.echo(
            "Failed importing aiohttp, did you "
            "forget to install it or activate an venv?",
            err=True,
        )
        exit(2)
    except KeyboardInterrupt:
        ...
    except Exception as e:
        click.echo(str(e), err=True)
        exit(1)


if __name__ == "__main__":
    main()
