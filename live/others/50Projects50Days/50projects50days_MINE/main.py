from aiohttp import web
from views import setup as views_setup
from uvloop import install as install_uvloop


async def application() -> web.Application:
    install_uvloop()
    app = web.Application()
    views_setup(app)
    return app