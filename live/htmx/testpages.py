from aiohttp_mako import template
from itertools import count
from aiohttp import web
import html

counter = count(1)

Count: int = 0


@template("testpages/home.mako")
async def index(req: web.Request):
    return {}


@template("testpages/test.mako")
async def test(req: web.Request):
    global Count
    Count += 1
    return {"Hello": "World", "Count": Count}


@template("testpages/nameform.mako")
async def nameform(req: web.Request):
    return {}


async def deletename(req: web.Request):
    return web.Response()


@template("testpages/showname.mako")
async def showname(req: web.Request):
    data = await req.post()
    name = data.get("name") or "anonymous"
    # return {'name': name, 'ID': next(counter)} # XSS Attack
    return {"name": html.escape(name), "ID": next(counter)}


routes: list[web.AbstractRouteDef] = [
    web.get("/test", index),
    web.get("/test/test", test),
    web.get("/test/nameform", nameform),
    web.get("/test/deletename", deletename),
    web.post("/test/showname", showname),
]
