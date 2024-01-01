from aiohttp import web
import time, base64
from mpack import flags
from aiohttp_security import (
    AbstractIdentityPolicy,
    AbstractAuthorizationPolicy,
    setup as _security_setup,
    remember
)
from .dataplugin import getappdata

_APP: web.Application

async def _basicauth_decode(token: str):
    _, etoken = token.split(" ")
    etoken = base64.urlsafe_b64decode(etoken.encode())
    user, _, passwd = etoken.decode().partition(":")
    return user, passwd


@web.middleware
async def _entrypoint(req: web.Request, handler):
    if (auth := req.headers.get("Authorization")) and auth.startswith("Basic "):
        username, password = await _basicauth_decode(auth)
        await remember(req, None, f'{username}:#:{password}')
    return await handler(req)

async def logreq(req: web.Request, resp: web.StreamResponse):
    def gettime():
        c = time.localtime(time.time())
        return f'{c.tm_mday}/{c.tm_mon}/{c.tm_year} {c.tm_hour % 12}:{c.tm_min}:{c.tm_sec} {"PM" if c.tm_hour > 12 else "AM"}'

    print(
        f"[{gettime()}] - {req.method} HTTP/{req.version.major}.{req.version.minor} - {req.path_qs} - {resp.status} {resp.reason!r}"
    )

class UserDataAuthPolicy(AbstractAuthorizationPolicy):        
    async def permits(self, identity: str, permission: int, context=None):
        manager = getappdata(_APP)
        username, _, _ = identity.partition(':#:')
        user = manager.users.get(username)
        if not user: return False
        perm = user.permission
        return flags.ison(perm, permission)

    async def authorized_userid(self, identity: str):
        manager = getappdata(_APP)
        username, _, password = identity.partition(':#:')
        if user := manager.users.get(username):
            if password == user.password:
                return user

class UserDataIdentityPolicy(AbstractIdentityPolicy):
    identity_key = "USER.IDENTITY"

    async def remember(self, request, response, identity, **kwargs):
        request[self.identity_key] = identity

    async def forget(self, request, response):
        if self.identity_key in request:
            del request[self.identity_key]

    async def identify(self, request):
        return request.get(self.identity_key)


def setup(app: web.Application):
    global _APP
    _APP = app
    _security_setup(app, UserDataIdentityPolicy(), UserDataAuthPolicy())
    app.middlewares.append(_entrypoint)
    app.on_response_prepare.append(logreq)