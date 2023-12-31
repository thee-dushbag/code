from aiohttp import web
from aiohttp_mako import setup
from mpack.aiohttp_helpers.auth import create_check_basic_auth
from utils import CHECK_AUTH_KEY, DB_STORE_KEY, DatabaseStore
from views import routes


def doThis(function, *args, **kwargs):
    async def noUseArgs(*_, **__):
        return function(*args, **kwargs)

    return noUseArgs


db: DatabaseStore = DatabaseStore("users.json")
app = web.Application()
app[DB_STORE_KEY] = db
app[CHECK_AUTH_KEY] = create_check_basic_auth(db)
setup(app, "./templates")
app.add_routes(routes)
app.on_shutdown.append(doThis(db.save_users))
app.on_startup.append(doThis(db.load_users))
