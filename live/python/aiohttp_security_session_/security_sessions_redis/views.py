from pathlib import Path
from aiohttp import web
from aiohttp_session import setup as sessions_setup, SimpleCookieStorage, get_session, new_session
from typing import Any
from aiomcache import Client as MemCacheClient
from cryptography.fernet import Fernet
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_session.redis_storage import RedisStorage
from aiohttp_session.memcached_storage import MemcachedStorage
from aiohttp_security.session_identity import SessionIdentityPolicy
from aiohttp_security.abc import AbstractAuthorizationPolicy
from redis.asyncio import Redis
from aiohttp_mako import setup as mako_setup, template
from time import time, localtime, asctime
from attrs import define, field
from uuid import uuid4
from aiohttp_security import (
    setup as security_setup,
    check_authorized,
    check_permission,
    remember, forget,
    authorized_userid
)
from enum import unique, StrEnum, auto

@unique
class Permission(StrEnum):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()


_uname = lambda name: str(name).lower().replace(" ", "_")
GENERATE_PASSWORD = 'generate_password'

@define
class User:
    username: str = field(converter=_uname)
    password: str = field(converter=str, eq=False)
    permissions: set[Permission] = field(converter=set, eq=False)
    
    def __attrs_post_init__(self):
        if self.password == GENERATE_PASSWORD:
            self.password = f'{self.username}Pass'

    def __hash__(self) -> int:
        return hash(self.username)


@define
class Users:
    users: set[User] = field(converter=set)

    def get_user(self, name: str) -> User | None:
        for user in self.users:
            if user.username == name:
                return user

    def add_user(self, user: User):
        if not self.get_user(user.username):
            self.users.add(user)
            return user


users = {
    User("simon", "simon5052", {Permission.WRITE, Permission.EXECUTE, Permission.READ}),
    User("lydia", GENERATE_PASSWORD, {Permission.WRITE, Permission.EXECUTE}),
    User("faith", GENERATE_PASSWORD, {Permission.READ, Permission.EXECUTE}),
    User("darius", GENERATE_PASSWORD, {Permission.WRITE, Permission.READ}),
    User("obed", GENERATE_PASSWORD, {Permission.EXECUTE}),
    User("david", GENERATE_PASSWORD, {Permission.WRITE}),
    User("shiro", GENERATE_PASSWORD, {Permission.READ}),
    User("losuru", GENERATE_PASSWORD, {}),
}

userdb = Users(users)

@define
class IdentityString:    
    def create_identity_string(self, user: User) -> str:
        return f'Identify.{uuid4().hex}.As.{user.username}'

    def get_user_from(self, identity_string: str) -> User | None:
        try:
            name = identity_string.split('.')[-1]
            return userdb.get_user(name)
        except Exception:
            pass

class AuthPolicy(AbstractAuthorizationPolicy):
    def __init__(self) -> None:
        self.identity_handler = IdentityString()

    async def permits(self, identity, permission, context=None):
        if user := self.identity_handler.get_user_from(identity):
            return permission in user.permissions

    async def authorized_userid(self, identity):
        return self.identity_handler.get_user_from(identity)


def string_time(_time=None):
    t = _time or time()
    timest = localtime(t)
    return asctime(timest)


WORKING_DIR = Path.cwd()
TEMPLATE_DIR = WORKING_DIR / "templates"


@template("index.mako")
async def index(req: web.Request):
    return {}

@template('userpage.mako')
async def userpage(req: web.Request):
    user = await check_authorized(req)
    return {'user': user}

async def logout(req: web.Request):
    await check_authorized(req)
    resp = web.HTTPSeeOther('/loginpage')
    await forget(req, resp)
    raise resp

async def login_post(req: web.Request):
    data = await req.post()
    username = str(data.get('username', ''))
    password = str(data.get('password', ''))
    if username:
        if user := userdb.get_user(username):
            if user.password == password:
                await new_session(req)
                resp = web.HTTPSeeOther('/userpage')
                identity = IdentityString().create_identity_string(user)
                await remember(req, resp, identity)
                raise resp
    raise web.HTTPSeeOther('/loginpage')

@template('login.mako')
async def loginpage(req: web.Request):
    return {}

@web.middleware
async def set_timming_middleware(req: web.Request, handler):
    session = await get_session(req)
    if "last-time" in session:
        session["visit-status"] = f"I have seen you before."
    else:
        session["visit-status"] = f"You are new here."
        session["new-time"] = string_time()
    session["last-time"] = string_time()
    return await handler(req)


@template("time.mako")
async def gettime(req: web.Request):
    session = await get_session(req)
    ntime = session.get("new-time", "New Time Not Found")
    status = session.get("visit-status", "Visit Status Not Found.")
    ltime = session.get("last-time", "Last Time Not Found")
    return dict(newtime=ntime, visitstatus=status, lasttime=ltime)


def message_handler(message: str, todo=None):
    @template('message.mako')
    async def handler(req: web.Request):
        if todo: await todo(req)
        return {'message':message}
    return handler

def permission_message(perm: Permission):
    msg = f'''<div>You can <span class="text-danger"><u>{perm}</u></span>. Permission Granted.</div>
        <a href="/userpage" class="d-block btn btn-link">Userpage</a>
    '''
    async def check_perm(req):
        await check_permission(req, perm)
    return message_handler(msg, check_perm)

@web.middleware
async def pretty_errors(req: web.Request, handler):
    try:
        return await handler(req)
    except web.HTTPForbidden as e:
        message = f'I Forbid you to access: {req.url.path}'
    except web.HTTPUnauthorized as e:
        raise web.HTTPSeeOther('/loginpage')
    except web.HTTPNotFound as e:
        message = f'''
            Resource {req.url.path} was not found.
            <div class="btn"></div>
        '''
    new_handler = message_handler(message)
    return await new_handler(req)

read_handler = permission_message(Permission.READ)
write_handler = permission_message(Permission.WRITE)
execute_handler = permission_message(Permission.EXECUTE)

routes: list = [
    web.get("/", index, name="home"), # type: ignore
    web.get("/time", gettime, name="time"), # type: ignore
    web.get('/userpage', userpage), # type: ignore
    web.get('/loginpage', loginpage), # type: ignore
    web.post('/login', login_post), # type: ignore
    web.get('/perm/read', read_handler), # type: ignore
    web.get('/perm/write', write_handler), # type: ignore
    web.get('/perm/execute', execute_handler), # type: ignore
    web.get('/logout', logout)
]


def setup(app: web.Application):
    f = Fernet(Fernet.generate_key())
    mako_setup(app, str(TEMPLATE_DIR))
    storage = SimpleCookieStorage(max_age=30)
    # storage = EncryptedCookieStorage(f)
    security_setup(app, SessionIdentityPolicy(), AuthPolicy())
    # storage = RedisStorage(Redis(), max_age=20)
    sessions_setup(app, storage)
    app.middlewares.append(set_timming_middleware)
    app.middlewares.append(pretty_errors) # type: ignore
    return app.add_routes(routes)
