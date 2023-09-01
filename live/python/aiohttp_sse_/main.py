from mpack import aiohttp_helpers as ah
from views import setup as views_setup
from aiohttp import web


async def application(*_, **__):
    app = web.Application()
    ah.cors_setup(app)
    ah.dev_setup(app)
    views_setup(app)
    return app