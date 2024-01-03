from aiohttp import web
from pathlib import Path


async def home(req: web.Request):
    raise web.HTTPPermanentRedirect("/home.html")


routes = [web.get("/", home), web.static("/", Path(__file__).parent / "static")]


async def app():
    app = web.Application()
    app.add_routes(routes)
    return app
