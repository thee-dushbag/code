import asyncio as aio

from aiohttp import hdrs, web
from mpack.aiohttp_helpers import cors_setup, dev_setup


async def index(req: web.Request):
    await aio.sleep(2)
    return web.Response(text="Hello World")


routes = [web.route(hdrs.METH_ANY, "/", index)]


async def application():
    app = web.Application()
    app.add_routes(routes)
    dev_setup(app)
    cors_setup(app)
    return app


def run():
    web.run_app(application(), host="localhost", port=5052)


if __name__ == "__main__":
    run()
