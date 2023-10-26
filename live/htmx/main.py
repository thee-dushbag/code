from aiohttp_mako import setup as mako_setup
from views import setup as views_setup
from aiohttp import web
import config as cfg

async def application() -> web.Application:
    app = web.Application()
    views_setup(app)
    mako_setup(app, str(cfg.TEMPLATE_DIR))
    return app
