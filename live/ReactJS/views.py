from pprint import pprint
from attrs import define, asdict
from typing import Type, TypeVar
from aiohttp import web
from mpack.aiohttp_helpers import cors_setup, dev_setup
from hi import hi as say_hi
from data import _DataView
import asyncio as aio
from random import randint

T = TypeVar("T")


@define
class User:
    name: str
    age: int


def construct(cls: Type[T], *keys, **kwargs) -> T | None:
    try:
        args = {key: kwargs[key] for key in keys}
        return cls(**args)
    except Exception as e:
        return None


class Users(list[User]):
    def json(self):
        return [asdict(user) for user in self]


users: Users = Users()


class UserView(web.View):
    async def get(self):
        return web.json_response({"users": users.json()})

    async def post(self):
        try:
            data = await self.request.json()
        except Exception:
            raise web.HTTPBadRequest(reason="Expected json Content")
        user = construct(User, "name", "age", **data)
        if user:
            users.append(user)
        else:
            raise web.HTTPBadRequest()
        return await self.get()


async def json_data(req: web.Request):
    return web.json_response(
        {
            "people": [
                {"name": "Simon Nganga", "age": 20, "school": "JKUAT"},
                {"name": "Faith Njeri", "age": 10, "school": "Horizon Learners"},
            ]
        }
    )


async def hi(req: web.Request):
    name = req.query.get("name", "stranger") or "stranger"
    return web.json_response({"greeting": say_hi(name.title())})


async def data_endpoint(req: web.Request):
    return web.json_response(
        dict(name="Simon Nganga", age=20, email="simongash@gmail.com")
    )


class DataView(_DataView):
    async def get(self):
        await aio.sleep(randint(1, 5))
        key = self.request.query.get("key", None)
        target = None
        if key is None:
            target = self.data.data
        elif key in self.data.data:
            target = self.data.data[key]
        else:
            raise web.HTTPBadRequest(
                reason=f"Data corresponding to {key!r} was not found."
            )
        return web.json_response(target)

    async def post(self):
        data = dict(await self.request.post())
        key = self.request.query.get("key", None) or None
        if key is None:
            raise web.HTTPBadRequest(reason=f"key cannot be None or empty string.")
        else:
            self.data.data[key] = data
            self.data.fresh()
        raise web.HTTPOk

    async def delete(self):
        key = self.request.query.get("key", None)
        target = None
        if key is None:
            raise web.HTTPBadRequest(reason="specify a key or pass an empty string.")
        elif key == "":
            target = self.data.data
            self.data.data = {}
        elif key in self.data.data:
            target = self.data.data[key]
            del self.data.data[key]
        else:
            raise web.HTTPBadRequest(
                reason=f"Data corresponding to {key!r} was not found."
            )
        self.data.fresh()
        return web.json_response(target)


routes = [
    web.view("/users", UserView),
    web.get("/js.json", json_data),
    web.get("/greet", hi),
    web.get("/datae", data_endpoint),
    web.view("/data", DataView),
]

@web.middleware
async def log_req(req: web.Request, handler):
    info = dict(req.headers)
    info.update(method=req.method)
    pprint(info)
    return await handler(req)

def setup(app: web.Application):
    app.middlewares.append(log_req)
    app.add_routes(routes)
    cors_setup(app)
    dev_setup(app)
