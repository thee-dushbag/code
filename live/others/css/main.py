from mpack.aiohttp_helpers import dev_setup, cors_setup
from views import setup as views_setup
from aiohttp import web


async def application() -> web.Application:
    app = web.Application()
    views_setup(app)
    cors_setup(app)
    dev_setup(app)
    return app
