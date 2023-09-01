from aiohttp import web
from views import setup as views_setup
from store import setup as store_setup

async def app_factory() -> web.Application:
    app = web.Application()
    store_setup(app)
    views_setup(app)
    return app