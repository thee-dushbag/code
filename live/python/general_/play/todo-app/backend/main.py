from aiohttp import web
from utils import setup as utils_setup
from views import setup as views_setup


async def app_factory() -> web.Application:
    app = web.Application()
    views_setup(app)
    utils_setup(app)
    return app
