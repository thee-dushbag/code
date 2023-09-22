from aiohttp import web
from uvloop import install as install_uvloop
from views import setup as views_setup


async def application() -> web.Application:
    install_uvloop()
    app = web.Application()
    views_setup(app)
    return app
