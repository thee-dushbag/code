import json
from random import choice
from typing import Callable, cast

import basicauth as bs
from aiohttp import web
from faker import Faker
from mpack import print
from mpack.aiohttp_helpers.mako_ import page_template
from utils import CHECK_AUTH_KEY, DB_STORE_KEY, DatabaseStore, User, UserData

fake = Faker()
page = page_template("page.mako")
routes = web.RouteTableDef()
routes.static("/static", "./static", name="static")


def hTag(v: int | None = None):
    u = [*range(1, 7)] if v is None else [v]
    return f"h{choice(u)}"


@routes.get(r"/headers/{n:\d+}")
@page("headers")
async def headers(req: web.Request):
    print(dict(req.headers))
    n = int(cast(str, req.match_info.get("n")))
    heads = [(hTag(), fake.sentence().title()) for _ in range(n)]
    return {"headers": heads}


@routes.get(r"/users/{n:\d+}")
@page("users")
async def users(req: web.Request):
    n = int(cast(str, req.match_info.get("n")))
    users = [User().to_dict().items() for _ in range(n)]
    return {"users": users}


@routes.route("*", "/user")
async def user(req: web.Request):
    auth = "Use BasicAuth Please"
    if auth_ := req.headers.get("Authorization"):
        auth = (
            "Authentication Successful"
            if bs.encode("simon", "simon_password") == auth_
            else "Authentication Unsuccessful"
        )
        auth = f"{auth} | {auth_}"
    return web.Response(text=auth)


@routes.route("*", "/get_auth")
async def get_auth(req: web.Request):
    auth = dict(status="Use BasicAuth Please")
    if auth_ := req.headers.get("Authorization"):
        try:
            username, password = bs.decode(auth_)
        except bs.DecodeError:
            auth["status"] = "Authentication Unsuccessful"
        else:
            auth["status"] = "Authentication Successful"
            auth["username"] = username
            auth["password"] = password
    return web.json_response(auth)


def ensure_valid_user(data, state=None):
    state = state or "Create"
    name, passwd = "username", "password"
    for prop in [name, passwd]:
        if not prop in data:
            raise web.HTTPUnauthorized(
                reason=f"Cannot {state} Account: {prop} not provided"
            )
        if not data.get(prop):
            raise web.HTTPUnauthorized(
                reason=f"Cannot {state} Account: {prop} has invalid value"
            )
    return data[name], data[passwd]


@routes.post("/add_user")
async def add_user(req: web.Request):
    db: DatabaseStore = req.app["user_database_store"]
    userdata: dict = cast(dict, await req.post())
    name, passwd = ensure_valid_user(dict(userdata))
    user = UserData(name, passwd)
    if db.add_user(user):
        return web.HTTPCreated(reason="User added Successfully")
    raise web.HTTPUnauthorized(reason=f"Username {name} already taken: Unsuccessful")


@routes.post("/rm_user")
async def rm_user(req: web.Request):
    db: DatabaseStore = req.app["user_database_store"]
    userdata: dict = cast(dict, await req.post())
    name, passwd = ensure_valid_user(dict(userdata), "Delete")
    if db.rm_user(name, passwd):
        raise web.HTTPCreated(reason="User deleted Successfully")
    raise web.HTTPUnauthorized(reason=f"Verification of {name} Unsuccessful")


@routes.view("/user_data_store", name="store")
class UserView(web.View):
    def __init__(self, request: web.Request) -> None:
        super().__init__(request)
        db: DatabaseStore = self.request.app[DB_STORE_KEY]
        check_auth: Callable[[web.Request], tuple[str, str]] = self.request.app[
            CHECK_AUTH_KEY
        ]
        userdata = check_auth(request)
        self.username = userdata[0]
        self.password = userdata[1]
        self.user = cast(UserData, db.get_user(self.username, self.password))

    async def get(self):
        key = self.request.query.get("key")
        data = self.user.data.get(key) if key else self.user.data
        data = {str(key): data} if key else data
        return web.json_response(data)

    async def ensure_json_dict(self):
        try:
            data = await self.request.json()
        except json.JSONDecodeError:
            return {}
        else:
            return data

    async def post(self):
        data = await self.ensure_json_dict()
        for key, value in data.items():
            if key not in self.user.data:
                self.user.data[key] = value
        keys = list(self.user.data.keys())
        return web.json_response(dict(keys=keys))

    async def delete(self):
        key = self.request.query.get("key")
        data = self.user.data.pop(key, None)
        return web.json_response(dict(data=data))

    async def put(self):
        data = await self.ensure_json_dict()
        for key, value in data.items():
            if key in self.user.data:
                self.user.data[key] = value
        keys = list(self.user.data.keys())
        return web.json_response(dict(keys=keys))
