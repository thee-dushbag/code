from aiohttp import web
from mpack.aiohttp_helpers import cors_setup, dev_setup
from views import setup as views_setup


async def application() -> web.Application:
    app = web.Application()
    views_setup(app)
    cors_setup(app)
    dev_setup(app)
    return app
