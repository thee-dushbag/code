from aiohttp import web
from pathlib import Path
from aiohttp_mako import setup as mako_setup
from uvloop import install as install_uvloop
from model_helpers import DatabaseManager
from model import setup as database_setup
from views import setup as views_setup
from security import NoteAppAuthPolicy
from aiohttp_session import setup as aio_session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography.fernet import Fernet
from aiohttp_security import (
    setup as aio_security_setup,
    SessionIdentityPolicy
)


WORKING_PATH = Path.cwd()
TEMPLATE_PATH = WORKING_PATH / 'templates'
STATIC_PATH = WORKING_PATH / 'static'
DNS = 'sqlite:///sessions.sqlite3'
SECRET_KEY = Fernet(Fernet.generate_key())
install_uvloop()


async def app_factory(tmp_path=None, static_path=None, dns=None) -> web.Application:
    app = web.Application()
    mako_setup(app, tmp_path or str(TEMPLATE_PATH))
    views_setup(app, str(STATIC_PATH))
    db = database_setup(app, dns or DNS)
    storage = EncryptedCookieStorage(SECRET_KEY)
    aio_session_setup(app, storage)
    identity_policy = SessionIdentityPolicy()
    manager = DatabaseManager(db)
    auth_policy = NoteAppAuthPolicy(manager)
    aio_security_setup(app, identity_policy, auth_policy)
    return app