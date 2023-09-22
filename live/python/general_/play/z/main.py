import asyncio as aio
from pathlib import Path

from aiohttp import web
from aiohttp_mako import setup as mako_setup
from aiohttp_mako import template
from aiohttp_sse import EventSourceResponse, sse_response
from mpack.number_reader import NumberReader
from mpack.number_reader.locales import english_locale

reader = NumberReader(english_locale)
WORKING_DIR = Path.cwd()
STATIC_DIR = WORKING_DIR / "static"
TEMPLATES_DIR = WORKING_DIR / "templates"


@template("home.mako")
async def home_page(req: web.Request):
    start, stop, read = 1, 2, reader.read
    get_url = lambda name: req.app.router[name].url_for()
    links = {read(n).title(): get_url(read(n)) for n in range(start, stop + 1)}
    return {"links": links}


@template("one.mako")
async def page_one(req: web.Request):
    return {}


@template("two.mako")
async def page_two(req: web.Request):
    return {}


counter = 0


async def sse(req: web.Request):
    global counter
    counter += 1
    print(f"[{counter}]: New Connection Made: {req}")
    async with sse_response(req) as resp:
        start, end = 1, 10
        rstart, rend = map(reader.read, (start, end))
        await resp.send(f"Counting from {rstart} to {rend}")
        for i in range(start, end + 1):
            name = reader.read(i).title()
            await aio.sleep(0.5)
            await resp.send(f"Count AT: {name}")
        await resp.send("Done Counting. Please Close!!!")
    print(f"[{counter}]: Connection Closed: {req}")
    return resp


routes = [
    web.get("/", home_page, name="home"),
    web.get("/one", page_one, name="one"),
    web.get("/two", page_two, name="two"),
    web.get("/sse", sse),
    web.static("/static", STATIC_DIR),
]


async def application() -> web.Application:
    app = web.Application()
    mako_setup(app, str(TEMPLATES_DIR))
    app.add_routes(routes)
    return app
