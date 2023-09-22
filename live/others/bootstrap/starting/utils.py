import functools
from typing import Any, Callable, Coroutine

from aiohttp import web
from aiohttp.web_routedef import _HandlerType
from aiohttp_mako import APP_KEY as MAKO_APP_KEY
from aiohttp_mako import render_template
from mpack.aiohttp_helpers.mako_ import uglify_html


def url_for(app: web.Application):
    def url(__name: str, **kwargs: str):
        loc = app.router[__name]
        return loc.url_for(**kwargs)

    return url


def template(
    template_name: str, *, app_key=MAKO_APP_KEY, encoding="utf-8", status=200
) -> Callable[..., _HandlerType]:
    def wrapper(func: Callable[[web.Request], Coroutine[Any, Any, dict[str, Any]]]):
        @functools.wraps(func)
        async def wrapped(*args):
            context: dict = await func(*args)
            request = args[-1]
            url = url_for(request.app)
            context = {"url": url, **context}
            response = render_template(
                template_name, request, context, app_key=app_key, encoding=encoding
            )
            # if response.text:
            # response.text = uglify_html(response.text)
            response.set_status(status)
            return response

        return wrapped

    return wrapper  # type: ignore[Any]
