from pathlib import Path

from aiohttp import web
from aiohttp_mako import setup as mako_setup
from model import setup as database_setup
from uvloop import install as install_uvloop
from views import setup as views_setup

CUR_DIR = Path.cwd()
TEMPLATES_PATH = CUR_DIR / "templates"
STATIC_PATH = CUR_DIR / "static"
DNS = "sqlite:///people.db"
install_uvloop()


async def app_factory(tmp_path=None, static_path=None, dns=None) -> web.Application:
    app = web.Application()
    mako_setup(app, tmp_path or str(TEMPLATES_PATH))
    views_setup(app, static_path or str(STATIC_PATH))
    database_setup(app, dns or DNS)
    return app
