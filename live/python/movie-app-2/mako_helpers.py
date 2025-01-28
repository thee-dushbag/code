from typing import Any, Awaitable, Callable, Coroutine, Mapping, cast
from mpack.line import aprint, Line

from aiohttp import hdrs, web
from aiohttp.typedefs import Handler
from aiohttp_mako import render_template, setup, APP_KEY
from aiohttp_mako import template as _template
from bs4 import BeautifulSoup
from css_html_js_minify import html_minify
from mako.lookup import TemplateLookup

FORMAT = '{remote_addr} - {time} {http_version} {code} - "{method} {path}"'
APP_KEY_LINE = web.AppKey("location_line")
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

def uglify_html(html_content: str, *, formatter=None, parser=None) -> str:
    import re

    soup = BeautifulSoup(html_content, parser or "lxml")
    prettified = soup.prettify(formatter=formatter or "html5")
    space = re.compile(r"\s+")
    return space.sub(" ", prettified)


ContextHandler = Callable[[web.Request], Coroutine[Any, Any, Mapping[str, Any]]]
InterHandler = Callable[[ContextHandler], Handler]
TemplateHandler = Callable[[str], InterHandler]
_ViewHandler = Callable[[Any], Awaitable[Mapping[str, Any]]]

mako_template = cast(TemplateHandler, _template)

def get_line(app: web.Application):
    if line := app.get(APP_KEY_LINE, None):
        return cast(Line, line)
    raise Exception("Please setup the debug. dev_setup(app)")

def _get_time() -> str:
    from time import localtime
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
async def print_request(req: web.Request, resp: web.StreamResponse):
    line = get_line(req.app)
    req_str = _get_request_string(req, resp)
    line.add_line(req_str)


async def _line_ctx(app: web.Application):
    async with Line(aprint, timeout=2) as line:
        app[APP_KEY_LINE] = line
        yield


def dev_setup(app: web.Application):
    app.on_response_prepare.append(print_request)
    app.cleanup_ctx.append(_line_ctx)


async def prepare_resp(_: web.Request, resp: web.StreamResponse):
    resp.headers[hdrs.ACCESS_CONTROL_ALLOW_CREDENTIALS] = "true"
    resp.headers[hdrs.ACCESS_CONTROL_ALLOW_HEADERS] = "*"
    resp.headers[hdrs.ACCESS_CONTROL_EXPOSE_HEADERS] = "*"
    resp.headers[hdrs.ACCESS_CONTROL_ALLOW_METHODS] = "*"
    resp.headers[hdrs.ACCESS_CONTROL_ALLOW_ORIGIN] = "*"


def cors_setup(app: web.Application):
    app.on_response_prepare.append(prepare_resp)


def template_handler(
    page_name: str, get_context=lambda r: {"request": r}, **context: Any
):
    @template(page_name)
    async def handler(req: web.Request):
        context.update(get_context(req))
        return context

    return handler


def template_view(page_name: str) -> Callable[..., Handler]:
    def _handler(func: _ViewHandler) -> Handler:
        async def _get_resp(_v) -> web.Response:
            context = await func(_v)
            resp = render_template(page_name, _v.request, context, app_key=str(APP_KEY))
            return resp

        return _get_resp

    return _handler


def template(page_name: str) -> Callable[..., Handler]:
    def _handler(func: _ViewHandler) -> Handler:
        async def _get_resp(req: web.Request) -> web.Response:
            context = await func(req)
            resp = render_template(page_name, req, context, app_key=str(APP_KEY))
            if resp.text:
                resp.text = html_minify(resp.text)
            return resp

        return _get_resp

    return _handler

