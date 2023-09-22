import security as sec
from aiohttp import web
from aiohttp_mako import setup as mako_setup
from models import DB_KEY, init_db
from views import routes


async def close_database(app: web.Application):
    print("Closing database.")
    app[DB_KEY].close()


app = web.Application()
Session = init_db("sqlite:///db.sqlite3")
app[DB_KEY] = Session()
mako_setup(app, "./templates")
app.add_routes(routes)

app.on_shutdown.append(close_database)
