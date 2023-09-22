import _views as cbs
import config as cfg
from aiohttp import web
from aiohttp_mako import setup as mako_setup
from config import Project

projects = [
    Project("index", "/", "index.mako", "Home Page", cbs.index),
    Project("zindex", "/zindex", "zindex.mako", "z-index project animations"),
    Project("layers", "/layers", "layers.mako", "layer animations"),
]

routes: list[web.AbstractRouteDef] = [
    web.static("/static", cfg.STATIC_DIR, name="static"),
    web.static("/public", cfg.PUBLIC_DIR, name="public"),
    *(project.routedef() for project in projects),
]


def setup(app: web.Application):
    mako_setup(app, str(cfg.TEMPLATE_DIR))
    return app.add_routes(routes)
