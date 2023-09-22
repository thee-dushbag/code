from pathlib import Path

from aiohttp import web
from aiohttp_mako import setup as mako_setup
from aiohttp_mako import template
from uvloop import install as install_uvloop
from views import setup as views_setup

install_uvloop()
CUR_DIR = Path.cwd()
TMP_PATH = CUR_DIR / "templates"
STATIC_PATH = CUR_DIR / "static"


async def app_factory(tmp_path=None) -> web.Application:
    app = web.Application()
    views_setup(app, str(STATIC_PATH))
    mako_setup(app, tmp_path or str(TMP_PATH))
    return app
