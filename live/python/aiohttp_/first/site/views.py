from typing import Any, cast

import utils as _u
from aiohttp import web
from aiohttp_mako import template
from model import manager_from_request


async def index(req: web.Request):
    resrc = req.app.router.get("people_page", None)
    if resrc is None:
        raise web.HTTPNotFound(reason="HomePage Not Setup")
    url = resrc.url_for(**req.query)
    raise web.HTTPSeeOther(url)


@template("people.mako")
async def people_page(req: web.Request):
    manager = manager_from_request(req)
    return {"persons": manager.get_all_people()}


async def add_person(req: web.Request):
    data = await req.post()
    name = _u.missing_or(str, data.get("name", _u.sentinel))
    age = _u.missing_or(str, data.get("age", _u.sentinel))
    email = _u.missing_or(str, data.get("email", _u.sentinel))
    personpage = req.app.router["people_page"].url_for()
    location = web.HTTPSeeOther(personpage)
    if any(map(_u.is_missing, (name, age, email))):
        raise location
    manager = manager_from_request(req)
    if manager.add_person(cast(str, name), cast(str, age), cast(str, email)):
        raise location
    raise location


async def delete_person(req: web.Request):
    manager = manager_from_request(req)
    pid = int(req.match_info.get("pid"))  # type:ignore
    manager.delete_person(pid)
    personpage = req.app.router["people_page"].url_for()
    return web.HTTPSeeOther(personpage)


def setup(app: web.Application, static_path: str):
    routes = [
        web.get("/", index, name="index"),
        web.static("/static", static_path, name="static"),
        web.get("/people_page", people_page, name="people_page"),  # type:ignore
        web.post("/add_person", add_person, name="add_person"),
        web.get(r"/delete_person/{pid:\d+}", delete_person, name="delete_person"),
    ]
    app.add_routes(routes)
    return routes
