import re
from typing import Any, Awaitable, Callable, Coroutine, Mapping, cast

from aiohttp import web
from aiohttp.typedefs import Handler
from aiohttp_mako import render_template
from aiohttp_mako import template as _template
from bs4 import BeautifulSoup
from css_html_js_minify import html_minify
from mako.lookup import TemplateLookup


def get_url(request: web.Request):
    def url(name: str, **kwargs):
        return request.app.router[name].url_for(
            **{k: str(v) for k, v in kwargs.items()}
        )

    return url


class MyDict:
    def __init__(self, _strict_: bool | None = None, **data) -> None:
        self.data = data
        self.strict = _strict_

    def __getattr__(self, __name: str) -> Any:
        if __name in self.data.keys():
            return self.data[__name]
        if self.strict:
            raise AttributeError("Not Defined: %s" % __name)


def uglify_html(html_content: str, *, formatter=None, parser=None) -> str:
    soup = BeautifulSoup(html_content, parser or "lxml")
    prettified = soup.prettify(formatter=formatter or "html5")
    space = re.compile(r"\s+")
    return space.sub(" ", prettified)


def page_template(
    page_template_file: str,
    *,
    page_key: str = "page",
    data_key: str = "data",
    global_key: str = "g"
):
    def get_template(page_name: str, **global_data):
        def wrapper(handler: Callable):
            async def get_data(req: web.Request):
                u_data: dict = await handler(req)
                u_data["request"] = req
                u_data["url"] = get_url(req)
                gbl_data = MyDict(**global_data)
                data = {
                    global_key: gbl_data,
                    page_key: page_name,
                    data_key: MyDict(**u_data),
                }
                res = render_template(page_template_file, req, data)
                if res.text:
                    res.text = html_minify(res.text)
                return res

            return get_data

        return wrapper

    return get_template


APP_KEY = "mako_helper.function.utils.unique.key"

ContextHandler = Callable[[web.Request], Coroutine[Any, Any, Mapping[str, Any]]]
InterHandler = Callable[[ContextHandler], Handler]
TemplateHandler = Callable[[str], InterHandler]
_ViewHandler = Callable[[Any], Awaitable[Mapping[str, Any]]]

mako_template = cast(TemplateHandler, _template)


def template_handler(page_name: str, **context: Any):
    @template(page_name)
    async def handler(req: web.Request):
        return context

    return handler


def template_view(page_name: str) -> Callable[..., Handler]:
    def _handler(func: _ViewHandler) -> Handler:
        async def _get_resp(_v) -> web.Response:
            context = await func(_v)
            resp = render_template(page_name, _v.request, context, app_key=APP_KEY)
            return resp

        return _get_resp

    return _handler


def template(page_name: str) -> Callable[..., Handler]:
    def _handler(func: _ViewHandler) -> Handler:
        async def _get_resp(req: web.Request) -> web.Response:
            context = await func(req)
            resp = render_template(page_name, req, context)
            if resp.text:
                resp.text = html_minify(resp.text)
            return resp

        return _get_resp

    return _handler


def setup(app: web.Application, path):
    lookup = TemplateLookup(path)
    app[APP_KEY] = lookup
    return lookup
