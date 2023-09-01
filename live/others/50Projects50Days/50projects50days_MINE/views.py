from aiohttp import web
import config as cfg
from config import Project
import _views as cbs
from aiohttp_mako import (
    setup as mako_setup
)

projects = [
    Project('index', '/', 'index.mako', 'Home Page', cbs.index),
    Project('progress_track', '/progress_track', 'progress_track.mako', 'Track Progress')
]

routes: list[web.AbstractRouteDef] = [
    web.static('/static', cfg.STATIC_DIR, name='static'),
    web.static('/fonts', cfg.FONT_DIR, name='fonts'),
    *(project.routedef() for project in projects)
]

def setup(app: web.Application):
    mako_setup(app, str(cfg.TEMPLATE_DIR))
    return app.add_routes(routes)