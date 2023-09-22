from pathlib import Path

import aiohttp_jinja2 as aji
from aiohttp import web
from jinja2 import FileSystemLoader
from model import init_db
from sqlalchemy.orm import Session as _Session
from usermanager import UserManager
from usite import USERSITE, UserSite
from views import routes

FORMAT = "utf-8"
TMP_PATH = Path.cwd() / "templates"
Session = init_db("sqlite:///users.db")
session = Session()


def create_app(template_path: str, session: _Session, app_key=None):
    manager = UserManager(session)
    usersite = UserSite(manager, FORMAT)
    app = web.Application()
    loader = FileSystemLoader(template_path)
    aji.setup(app, loader=loader)
    app[app_key or USERSITE] = usersite
    return app


app = create_app(str(TMP_PATH), session)
app.add_routes(routes)
