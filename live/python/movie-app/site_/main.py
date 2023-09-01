from uvloop import install as install_uvloop
from mpack.aiohttp_helpers import cors_setup, dev_setup
from views import setup as views_setup
from aiohttp import web
from movies import setup as movie_setup

async def application() -> web.Application:
    install_uvloop()
    app = web.Application()
    mov = movie_setup(app)
    cors_setup(app)
    dev_setup(app)
    views_setup(app, mov)
    return app

if __name__ == '__main__':
    from os import getenv
    HOST = getenv('MOVIE_HOST')
    PORT = int(getenv("MOVIE_PORT") or 5052)
    web.run_app(application(), host=HOST, port=PORT)