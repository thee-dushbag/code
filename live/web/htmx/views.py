from aiohttp import web
import config as cfg
from testpages import routes as test_routes

routes: list[web.AbstractRouteDef] = [
    *test_routes,
    web.static("/static", cfg.STATIC_DIR),
]


def setup(app: web.Application):
    app.add_routes(routes)
