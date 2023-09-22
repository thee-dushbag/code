from pathlib import Path

from aiohttp import web
from data import setup as data_setup
from gview import setup as gview_setup
from views import setup as views_setup

WORKING_DIR = Path(__file__).parent
DATA_PATH = WORKING_DIR / "data.json"


async def application() -> web.Application:
    app = web.Application()
    data_setup(app, DATA_PATH)
    gview_setup(app)
    views_setup(app)
    return app
