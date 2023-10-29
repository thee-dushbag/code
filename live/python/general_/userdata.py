from aiohttp import web
import enum, time, base64, json
from mpack import flags
from aiohttp_security import (
    AbstractIdentityPolicy,
    AbstractAuthorizationPolicy,
    setup as security_setup,
    check_permission,
)
from pathlib import Path
from dataclasses import dataclass


class Perm(enum.IntFlag):
    NONE: int = enum.auto(0)
    READ_DATA: int = enum.auto()
    WRITE_DATA: int = enum.auto()
    DELETE_DATA: int = enum.auto()
    READ_USER: int = enum.auto()
    WRITE_USER: int = enum.auto()
    DELETE_USER: int = enum.auto()


USERS = {}
DATA = None


def sldata(path: Path):
    async def job(_: web.Application):
        global DATA, USERS
        if not path.exists():
            path.touch()
            path.write_text("{}")
        data = json.loads(path.read_text())
        USERS = data.get("users", {})
        DATA = data.get("data", None)
        yield
        path.write_text(json.dumps({"users": USERS, "data": DATA}, indent=2))

    return job

_sentinel = object()

@dataclass
class AuthInfo:
    username: str = _sentinel
    password: str = _sentinel

    def authenticate(self):
        if user := USERS.get(self.username):
            if self.password == user.get("password", None):
                return True

    def __bool__(self):
        return bool(self.authenticate())


class UserDataAuthPolicy(AbstractAuthorizationPolicy):
    async def permits(self, identity: AuthInfo, permission: int, context=None):
        user = USERS.get(identity.username)
        if not user: return False
        perm = user.get("permission", Perm.NONE)
        return flags.flag_enabled(perm, permission)

    async def authorized_userid(self, identity: AuthInfo):
        return identity.authenticate()


class UserDataIdentityPolicy(AbstractIdentityPolicy):
    identity_key = "USER.IDENTITY"

    async def remember(self, request, response, identity, **kwargs):
        request[self.identity_key] = identity

    async def forget(self, request, response):
        if self.identity_key in request:
            del request[self.identity_key]

    async def identify(self, request):
        return request.get(self.identity_key)


async def logreq(req: web.Request, resp: web.StreamResponse):
    def gettime():
        c = time.localtime(time.time())
        return f'{c.tm_mday}/{c.tm_mon}/{c.tm_year} {c.tm_hour % 12}:{c.tm_min}:{c.tm_sec} {"PM" if c.tm_hour > 12 else "AM"}'

    print(
        f"[{gettime()}] - {req.method} HTTP/{req.version.major}.{req.version.minor} - {req.path_qs} - {resp.status} {resp.reason!r}"
    )


class UsersView(web.View):
    async def post(self):
        data = await self.request.post()
        if not (username := data.get("username")):
            raise web.HTTPBadRequest(reason="Username not provided.")
        if username in USERS:
            raise web.HTTPConflict(reason=f"User with {username!r} already exists.")
        if not (password := data.get("password")):
            raise web.HTTPBadRequest(
                reason=f"Password not provided for account {username!r}"
            )
        USERS[str(username)] = dict(password=str(password), permission=Perm.READ_DATA)
        raise web.HTTPCreated(reason=f"Account created for user {username!r}")

    async def put(self):
        await check_permission(self.request, Perm.WRITE_USER)
        user = self.request.query.get("user", None)
        if user is None:
            raise web.HTTPBadRequest(reason="Username not provided")
        elif target_user := USERS.get(user):
            data = await self.request.post()
            password = data.get("password", None)
            permission = data.get("permission", None)
            if permission is not None:
                if not permission.isnumeric():
                    raise web.HTTPBadRequest(
                        reason=f"Expected an integer value for permission, found: {permission!r}"
                    )
                target_user["permission"] = abs(int(permission))
            if password is not None:
                target_user["password"] = password
        else:
            raise web.HTTPNotFound(reason=f"No user with username {user!r}.")
        return web.HTTPAccepted(reason="Operation was successful")

    async def delete(self):
        await check_permission(self.request, Perm.DELETE_USER)
        user = self.request.query.get("user", None)
        if user is None:
            raise web.HTTPBadRequest(reason="Username not provided")
        elif user in USERS:
            userdata = USERS[user]
            del USERS[user]
            userdata["username"] = user
            return web.json_response({"user": user})
        else:
            raise web.HTTPNotFound(reason=f"No user with username {user!r}.")

    async def get(self):
        await check_permission(self.request, Perm.READ_USER)
        user = self.request.query.get("user", None)
        if user is None:
            payload = {"users": USERS}
        elif target_user := USERS.get(user):
            payload = {user: target_user}
        else:
            raise web.HTTPNotFound(reason=f"User with username {user!r} was not found.")
        return web.json_response(payload)


class DataView(web.View):
    async def get(self):
        await check_permission(self.request, Perm.READ_DATA)
        return web.json_response({"data": DATA})

    async def post(self):
        await check_permission(self.request, Perm.WRITE_DATA)
        data = await self.request.post()
        if ndata := data.get("data"):
            global DATA
            DATA = ndata
            return web.HTTPCreated(reason='New data was set.')
        raise web.HTTPBadRequest(reason="No data was sent.")

    async def delete(self):
        await check_permission(self.request, Perm.DELETE_DATA)
        global DATA
        data = DATA
        DATA = None
        return web.json_response({"result": data})


async def _basicauth_decode(token: str):
    _, etoken = token.split(" ")
    etoken = base64.urlsafe_b64decode(etoken.encode())
    user, _, passwd = etoken.decode().partition(":")
    return user, passwd


@web.middleware
async def _entrypoint(req: web.Request, handler):
    if (auth := req.headers.get("Authorization")) and auth.startswith("Basic "):
        username, password = await _basicauth_decode(auth)
        authinfo = AuthInfo(username=username, password=password)
        req[UserDataIdentityPolicy.identity_key] = authinfo
    return await handler(req)


routes = [web.view("/data", DataView), web.view("/user", UsersView)]


async def application():
    app = web.Application()
    app.on_response_prepare.append(logreq)
    app.cleanup_ctx.append(sldata(Path("usersdata.ignore.json")))
    app.middlewares.append(_entrypoint)
    security_setup(app, UserDataIdentityPolicy(), UserDataAuthPolicy())
    app.add_routes(routes)
    return app
