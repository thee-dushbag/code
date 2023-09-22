from aiohttp import web
from azdev import setup as azdev_setup

routes = []


def setup(app: web.Application):
    app.add_routes(routes)
    azdev_setup(app, prefix="/graphql")
