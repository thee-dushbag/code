import functools

from aiohttp import web
from aiohttp_mako import APP_KEY as MAKO_APP_KEY
from aiohttp_mako import render_template


def url_for(app: web.Application):
    def url(name: str, **kwargs: str):
        loc = app.router[name]
        return loc.url_for(**kwargs)

    return url


def template(template_name, *, app_key=MAKO_APP_KEY, encoding="utf-8", status=200):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args):
            context: dict = await func(*args)
            request = args[-1]
            url = url_for(request.app)
            context = {"url": url, **context}
            response = render_template(
                template_name, request, context, app_key=app_key, encoding=encoding
            )
            response.set_status(status)
            return response

        return wrapped

    return wrapper
