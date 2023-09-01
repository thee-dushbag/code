from aiohttp import web
from .db import init_db

APP_KEY = 'db.models.application.azdev.database.api'

def setup(app: web.Application):
    db = init_db(app['config']['dns'])
    app[APP_KEY] = db
    return db