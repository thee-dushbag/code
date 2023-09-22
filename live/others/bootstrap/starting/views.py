from pathlib import Path
from typing import Callable, Coroutine, cast

import httpx
from aiohttp import web
from faker import Faker
from utils import template, url_for
from yarl import URL

HOST, PORT = "192.168.0.100", 9944
faker_site = URL(f"http://{HOST}:{PORT}")

url: Callable[..., URL]
fake = Faker()
routes = web.RouteTableDef()


@routes.get("/hello", name="hello")
@template("hello.mako")
async def hello_page(req: web.Request):
    name = req.query.get("name", "stranger")
    return {"name": name}


@routes.post("/hello-post", name="hello_form")
async def hello_to(req: web.Request):
    data = await req.post()
    name = cast(str, data.get("name", "stranger"))
    loc = url("hello")
    if name:
        loc = loc.with_query(name=name)
    raise web.HTTPSeeOther(loc)


@routes.get("/typo")
@template("typography.mako")
async def typography(req: web.Request):
    return {}


@routes.get("/images")
@template("images.mako")
async def images(req: web.Request):
    return {}


@routes.get("/grid", name="grid")
@template("grid.mako")
async def grid(req: web.Request):
    return {}


@routes.get("/util")
@template("utilities.mako")
async def utilities(req: web.Request):
    return {}


@routes.get("/table")
@template("tables.mako")
async def tables(req: web.Request):
    return {}


def get_text(words=3):
    sentence_url = faker_site / "faker" / "sentence"
    url = sentence_url.with_query(nb_words=words, variable_nb_words="")
    resp = httpx.get(str(url))
    return resp.json().get("result", "Result Not Found in faker_site_sentence")


@routes.get("/cards", name="cards")
@template("cards.mako")
async def cards(req: web.Request):
    return {"fake_text": get_text}


@routes.get("/buttons", name="buttons")
@template("buttons.mako")
async def buttons(req: web.Request):
    return {}


@routes.get("/navs", name="navs")
@template("navs.mako")
async def navs(req: web.Request):
    return {}


@routes.get("/alerts", name="alerts")
@template("alerts.mako")
async def alerts(req: web.Request):
    return {}


def setup(app: web.Application, static_path: str):
    global url
    url = url_for(app)
    path = Path(static_path) / "image.png"
    path.write_bytes(fake.image((256, 256), "png"))
    routes.static("/static", static_path, name="static")
    app.add_routes(routes)
    return routes
