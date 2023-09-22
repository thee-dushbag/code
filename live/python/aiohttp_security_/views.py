import attrs
import db
import db_utils
from aiohttp import web
from aiohttp.web_request import Request


async def index(req: web.Request):
    return web.Response(text="Hello World")


routes = [
    web.get("/", index, name="index"),
]


def setup(app: web.Application):
    app.add_routes(routes)
