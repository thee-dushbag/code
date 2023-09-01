from aiohttp import web, hdrs
from pathlib import Path

WORKING_DIR = Path(__file__).parent
STATIC_DIR = WORKING_DIR / 'static'
PUBLIC_DIR = WORKING_DIR / 'public'

async def index(req: web.Request):
    return web.Response(body="Hello World")

routes = [
    web.route(hdrs.METH_ANY, '/', index),
    web.static('/static', STATIC_DIR),
    web.static('/public', PUBLIC_DIR),
]

def setup(app: web.Application):
    app.add_routes(routes)