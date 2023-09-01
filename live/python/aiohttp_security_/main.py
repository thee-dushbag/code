from aiohttp import web
from db import setup as db_setup
from data import setup as data_setup
from views import setup as views_setup

db_file_json = './users_resrc.json'

async def app_factory() -> web.Application:
    app = web.Application()
    db_setup(app, db_file_json)
    data_setup(app, False)
    views_setup(app)
    return app