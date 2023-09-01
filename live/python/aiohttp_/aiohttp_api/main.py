from aiohttp import web
from views import setup as views_setup
from model import setup as model_setup
from security import setup as security_setup
from uvloop import install as install_uvloop

DB_DNS = 'sqlite:///api_database.db'

async def app_factory() -> web.Application:
    install_uvloop()
    app = web.Application()
    db = model_setup(app, DB_DNS)
    # security_setup(app, db)
    views_setup(app)
    return app