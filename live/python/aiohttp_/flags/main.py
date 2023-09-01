from uvloop import install as install_uvloop
from security import setup as security_setup
from views import setup as views_setup
from db import setup as db_setup
from aiohttp import web

DNS = 'sqlite:///users.db'
MAX_AGE = 100

async def application() -> web.Application:
    install_uvloop()
    app = web.Application()
    views_setup(app)
    db = db_setup(app, DNS)
    security_setup(app, db, MAX_AGE)
    return app