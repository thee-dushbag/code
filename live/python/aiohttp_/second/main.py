from aiohttp import web
from store import setup as store_setup
from views import setup as views_setup


async def app_factory() -> web.Application:
    app = web.Application()
    store_setup(app)
    views_setup(app)
    return app
