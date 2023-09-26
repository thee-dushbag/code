from mpack.aiohttp_helpers.mako_ import setup as mako_setup
from mpack.aiohttp_helpers import cors_setup, dev_setup
from config import setup as config_setup
from movies import setup as movies_setup
from views import setup as views_setup
from aiohttp import web
import config as cfg

async def application() -> web.Application:
    app = web.Application()
    mako_setup(app, str(cfg.TEMPLATE_DIR))
    config = config_setup(app)
    movies_setup(app, config)
    views_setup(app)
    cors_setup(app)
    dev_setup(app)
    return app
