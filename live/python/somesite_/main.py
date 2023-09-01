from aiohttp import web
from time import asctime, localtime
from aiohttp_session import setup, get_session, Session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography.fernet import Fernet
import uvloop

uvloop.install()

async def set_last_visit(session: Session, key: str | None = None) -> str:
    skey: str = key or 'last_visit'
    now = asctime(localtime())
    print(f'setting last last_visit for: {session.identity}')
    if skey not in session:
        now += ' | New Comer'
    session[skey] = now
    return now


async def handler(req: web.Request):
    session = await get_session(req)
    last_visit = await set_last_visit(session)
    text = f'Last visited: {last_visit}'
    return web.Response(text=text)


async def make_app():
    app = web.Application()
    fernet_key = Fernet.generate_key()
    setup(app, EncryptedCookieStorage(fernet_key))
    app.add_routes([web.get('/', handler)])
    return app


web.run_app(make_app(), host='localhost', port=5052)