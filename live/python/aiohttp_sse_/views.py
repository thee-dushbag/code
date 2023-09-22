from pathlib import Path

from aiohttp import hdrs, web

WORKING_PATH = Path(__file__).parent
STATICS_PATH = WORKING_PATH / "static"


async def index(req: web.Request):
    return web.Response(text="Hello World")


routes = [web.static("/static", STATICS_PATH), web.route(hdrs.METH_ANY, "/", index)]


def setup(app: web.Application):
    app.add_routes(routes)
