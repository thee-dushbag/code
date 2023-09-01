from aiohttp import web
from views import setup as views_setup
from gview import setup as gview_setup
from data import setup as data_setup
from pathlib import Path

WORKING_DIR = Path(__file__).parent
DATA_PATH = WORKING_DIR / 'data.json'

async def application() -> web.Application:
    app = web.Application()
    data_setup(app, DATA_PATH)
    gview_setup(app)
    views_setup(app)
    return app