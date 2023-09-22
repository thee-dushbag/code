# type:ignore[assgnment]
from base64 import urlsafe_b64encode
from pathlib import Path

from aiohttp import web
from aiohttp_mako import setup as mako_setup
from aiohttp_mako import template
from aiohttp_session import SimpleCookieStorage, get_session
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography.fernet import Fernet

routes = web.RouteTableDef()
WORKING_DIR = Path.cwd()
TEMPLATE_DIR = WORKING_DIR / "templates"
STATIC_DIR = WORKING_DIR / "static"


@routes.get("/")
@template("hello.mako")
async def index(req: web.Request):
    return {}


@web.middleware
async def add_messages(req: web.Request, handler) -> web.Response:
    session = await get_session(req)
    session.setdefault("messages", [])
    return await handler(req)


def messages_setup(app: web.Application):
    app.middlewares.append(add_messages)


@routes.get("/send_text")
@template("msg.mako")
async def send_text(req: web.Request):
    session = await get_session(req)
    messages = session.get("messages")
    return {"msgs": messages}


@routes.post("/recv_text")
async def recv_text(req: web.Request):
    data = await req.post()
    session = await get_session(req)
    messages = session.get("messages")
    new_msg = data.get("msg", None)
    if new_msg:
        messages.append(new_msg)
    session._changed = True
    raise web.HTTPSeeOther("/send_text")


async def app_factory() -> web.Application:
    app = web.Application()
    routes.static("/static", STATIC_DIR)
    mako_setup(app, str(TEMPLATE_DIR))
    # secret_key = Fernet.generate_key()
    secret_key = urlsafe_b64encode(b"My Name is Simon Nganga Njoroge.")
    fernet_secret_key = Fernet(secret_key)
    storage = EncryptedCookieStorage(fernet_secret_key)
    session_setup(app, storage)
    messages_setup(app)
    app.add_routes(routes)
    return app
