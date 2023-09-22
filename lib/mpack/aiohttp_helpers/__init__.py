from time import localtime
from typing import cast

from aiohttp import hdrs
from aiohttp import typedefs as _t
from aiohttp import web

from ..line import Line, aprint

SUBSCRIBE = "subscribe"
UNSUBSCRIBE = "unsubscribe"
FORMAT = '{remote_addr} - {time} {http_version} {code} - "{method} {path}"'
APP_KEY = "mpack.aiohttp_helpers.__init__.utils"
MONTHS = (
    "jan",
    "feb",
    "mar",
    "april",
    "may",
    "june",
    "july",
    "aug",
    "sept",
    "oct",
    "nov",
    "dec",
)


def _get_time() -> str:
    t = localtime()
    tday = f"{t.tm_hour}:{t.tm_min}:{t.tm_sec}"
    tyear = f"{t.tm_mday}/{MONTHS[t.tm_mon - 1].title()}/{t.tm_year}"
    return f"[{tyear} {tday}]"


def _get_request_string(req: web.Request, resp: web.StreamResponse):
    v = req.version
    remote = "127.0.0.1" if req.remote == "::1" else req.remote
    return FORMAT.format(
        time=_get_time(),
        method=req.method,
        path=req.path_qs,
        http_version=f"HTTP{v.major}.{v.minor}",
        code=resp.status,
        remote_addr=remote or "",
    )


def subscribe(path: str, handler: _t.Handler, **kwargs):
    return web.route(SUBSCRIBE, path, handler, **kwargs)


def unsubscribe(path: str, handler: _t.Handler, **kwargs):
    return web.route(UNSUBSCRIBE, path, handler, **kwargs)


async def prepare_resp(_: web.Request, resp: web.StreamResponse):
    resp.headers[hdrs.ACCESS_CONTROL_ALLOW_CREDENTIALS] = "true"
    resp.headers[hdrs.ACCESS_CONTROL_ALLOW_HEADERS] = "*"
    resp.headers[hdrs.ACCESS_CONTROL_EXPOSE_HEADERS] = "*"
    resp.headers[hdrs.ACCESS_CONTROL_ALLOW_METHODS] = "*"
    resp.headers[hdrs.ACCESS_CONTROL_ALLOW_ORIGIN] = "*"


def cors_setup(app: web.Application):
    app.on_response_prepare.append(prepare_resp)


def get_line(app: web.Application):
    if line := app.get(APP_KEY, None):
        return cast(Line, line)
    raise Exception("Please setup the debug. dev_setup(app)")


async def print_request(req: web.Request, resp: web.StreamResponse):
    line = get_line(req.app)
    req_str = _get_request_string(req, resp)
    line.add_line(req_str)


async def _line_ctx(app: web.Application):
    async with Line(aprint, timeout=2) as line:
        app[APP_KEY] = line
        yield


def dev_setup(app: web.Application):
    app.on_response_prepare.append(print_request)
    app.cleanup_ctx.append(_line_ctx)
