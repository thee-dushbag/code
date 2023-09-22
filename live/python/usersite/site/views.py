import pprint
from pathlib import Path
from typing import cast

import aiohttp_jinja2 as aji
from aiohttp import web
from exc import State
from utils import get_user_site as gus
from utils import logged_in

STATIC_PATH = Path.cwd() / "static"
routes = web.RouteTableDef()
routes.static("/static", STATIC_PATH, name="static")


def redirect(req: web.Request, loc: str, **data: str | int):
    return web.HTTPSeeOther(
        req.app.router[loc].url_for(**{k: str(v) for k, v in data.items()})
    )


@routes.get("/", name="index")
@aji.template("page.html")
async def index(req: web.Request):
    site = gus(req)
    pprint.pprint(site.logged_in)
    return {"page": "home"}


@routes.get("/login", name="login")
@aji.template("page.html")
async def login(req: web.Request):
    return {"page": "login"}


@routes.post("/login_post", name="login_post")
async def login_post(req: web.Request):
    site = gus(req)
    data = await req.post()
    name = cast(str, data.get("name", ""))
    pword = cast(str, data.get("password", ""))
    status = site.login(name=name, password=pword)
    if status.state == State.SUCCESS:
        uid = site.manager.get_userid(name).result
        return redirect(req, "user", uid=uid)
    return redirect(req, "login")


@routes.post("/signup_post", name="signup_post")
async def signup_post(req: web.Request):
    site = gus(req)
    data = await req.post()
    name = cast(str, data.get("name", ""))
    pword = cast(str, data.get("password", ""))
    email = cast(str, data.get("email", ""))
    status = site.signup(name=name, password=pword, email=email)
    if status.state == State.SUCCESS:
        return redirect(req, "login")
    return redirect(req, "signup")


@routes.post(r"/cpword_post/{uid:\d+}", name="cpword_post")
async def cpword_post(req: web.Request):
    site = gus(req)
    uid = int(req.match_info.get("uid", -1))
    if not logged_in(req, uid):
        raise web.HTTPSeeOther(req.app.router["index"].url_for())
    data = await req.post()
    name = gus(req).manager.get_user(uid).result.name
    op = cast(str, data.get("old_password", ""))
    np = cast(str, data.get("new_password", ""))
    site.change_password(name, op, np)
    return redirect(req, "user", uid=uid)


@routes.get("/signup", name="signup")
@aji.template("page.html")
async def signup(req: web.Request):
    return {"page": "signup"}


@routes.get(r"/delete_post/{uid:\d+}", name="delete")
async def delet_acc(req: web.Request):
    uid = int(req.match_info.get("uid", -1))
    if not logged_in(req, uid):
        raise web.HTTPSeeOther(req.app.router["index"].url_for())
    site = gus(req)
    user = site.manager.get_user(uid, remove=True)
    if user.result.name in site.logged_in:
        site.logged_in.pop(user.result.name)
    raise web.HTTPSeeOther(req.app.router["index"].url_for())


@routes.get(r"/user/{uid:\d+}", name="user")
@aji.template("page.html")
async def user(req: web.Request):
    uid = int(req.match_info.get("uid", -1))
    if not logged_in(req, uid):
        raise web.HTTPSeeOther(req.app.router["index"].url_for())
    site = gus(req)
    user = site.manager.get_user(uid)
    return {"page": "user", "data": {"uid": uid, "name": user.result.name.title()}}


@routes.get(r"/logout/{uid:\d+}", name="logout")
async def logout(req: web.Request):
    uid = int(req.match_info.get("uid", -1))
    if not logged_in(req, uid):
        raise redirect(req, "index")
    site = gus(req)
    user = site.manager.get_user(uid).result.name
    if user in site.logged_in:
        site.logged_in.pop(user)
    raise redirect(req, "index")
