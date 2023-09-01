from mpack.aiohttp_helpers import dev_setup, cors_setup
from views import setup as views_setup
from aiohttp import web
import yaml, pathlib

WORKING_DIR = pathlib.Path(__file__).parent
CONFIG_FILE = WORKING_DIR / 'config.yml'

with CONFIG_FILE.open() as file:
    config = yaml.safe_load(file)

async def application():
    app = web.Application()
    app['config'] = config
    views_setup(app)
    cors_setup(app)
    dev_setup(app)
    return app
