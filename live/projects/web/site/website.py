from pprint import pprint
from aiohttp import web
import aiohttp_jinja2 as aji
from jinja2 import FileSystemLoader
from pathlib import Path

TEMPLATE_DIR = Path(Path.cwd() / "templates")
app = web.Application()
loader = FileSystemLoader(TEMPLATE_DIR)
ENV = aji.setup(app, loader=loader)
CSRF_TOKEN = "MainServerCSRFTOKENAuth0"


@aji.template("home.html")
async def index(req: web.Request):
    return {"csrf_token": CSRF_TOKEN}


@aji.template("greet.html")
async def greet(req: web.Request):
    name = "Stranger"
    name = req.match_info.get("name", name).title() or name
    return {"name": name}


async def greet_post(req: web.Request):
    data = await req.post()
    name = data.get("name", "")
    pprint(dict(data))
    location = req.app.router['greet'].url_for(name=name)
    raise web.HTTPSeeOther(location)


app.add_routes(
    (
        web.get("/", index, name="index"),
        web.get("/greet/{name:.*}", greet, name="greet"),
        web.post("/greet_post", greet_post, name="greet_post"),
    )
)
