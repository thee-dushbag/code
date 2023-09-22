from aiohttp import web
from config import setup as config_setup
from settings import config_registry
from uvloop import install as install_uvloop
from views import setup as views_setup

install_uvloop()


async def app_factory() -> web.Application:
    app = web.Application()
    config_setup(app, config_registry)
    views_setup(app)
    return app
