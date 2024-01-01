from pathlib import Path
from typing import cast

import db as _db
import security as _sc
from aiohttp import web
from aiohttp_mako import setup as mako_setup
from aiohttp_mako import template as _temp
from aiohttp_security import (check_authorized, check_permission, forget,
                              remember)
from mpack import flags
from mpack.aiohttp_helpers.mako_ import TemplateHandler, template_handler

# constants
WORKING_DIR = Path(__file__).parent
TEMPLATE_DIR = WORKING_DIR / "template"
STATIC_DIR = WORKING_DIR / "static"
template = cast(TemplateHandler, _temp)

# handlers
index = template_handler("index.mako")
_base = template_handler("base.mako")
login_page = template_handler("login.mako")
signup_page = template_handler("signup.mako")
_perms = [name.lower() for name in _db.Perm.interpret(0)]
_rperms = f"perm:({'|'.join(_perms)})"
_perm_page_regex = lambda base: f"/{base}" + "/{{}}".replace("{}", _rperms)


@template("perm.mako")
async def perm(req: web.Request):
    user = await check_authorized(req)
    sperm = req.match_info.get("perm", "")
    if perm := _db.Perm.get(sperm):
        g = _db.Perm.interpret(user.permission)[perm.name]
        return {"perm": perm.name, "granted": g, "user": user}
    raise web.HTTPNotFound(reason=f"Permission: {sperm} was not found.")


async def logout(req: web.Request):
    await check_authorized(req)
    resp = web.HTTPSeeOther("/")
    await forget(req, resp)
    raise resp


@template("userpage.mako")
async def userpage(req: web.Request):
    user = await check_authorized(req)
    return {"user": user, "perms": _db.Perm.interpret(user.permission)}


async def update_perm(req: web.Request):
    user = await check_authorized(req)
    data = await req.post()
    perms = {name: str(data.get(name, "off")) for name in _perms}
    values = [
        (_db.Perm.NONE if v == "off" else _db.Perm.get(n)) for n, v in perms.items()
    ]
    perm = _db.Perm.NONE
    for v in values:
        if v is not None:
            perm = flags.turnon(perm, v)
    db = _db.get_db(req)
    user.permission = perm
    db.update_user(user)
    raise web.HTTPSeeOther("/user")


async def login(req: web.Request):
    data = await req.post()
    username = str(data.get("username"))
    password = str(data.get("password"))
    db = _db.get_db(req)
    if user := db.get_user_by_name(username):
        if _db.check_password(password, str(user.password)):
            resp = web.HTTPSeeOther("/user")
            identity = await _sc.create_key(user)
            await remember(req, resp, identity)
            raise resp
    raise web.HTTPSeeOther("/login")


async def signup(req: web.Request):
    data = await req.post()
    username = str(data.get("username"))
    password = str(data.get("password"))
    useremail = str(data.get("useremail"))
    if not all((username, password, useremail)):
        raise web.HTTPSeeOther("/signup")
    db = _db.get_db(req)
    try:
        user = _db._md.Users(
            name=username, password=password, email=useremail, permission=_db.Perm.NONE
        )
        db.add_user(user)
        resp = web.HTTPSeeOther("/login")
    except Exception as e:
        resp = web.HTTPSeeOther("/signup")
    raise resp


@template("perm.mako")
async def test_perm(req: web.Request):
    user = await check_authorized(req)
    sperm = req.match_info.get("perm", "")
    if perm := _db.Perm.get(sperm):
        await check_permission(req, perm)
        g = _db.Perm.interpret(user.permission)[perm.name]
        return {"perm": perm.name, "granted": g, "user": user}
    raise web.HTTPNotFound(reason=f"Permission: {sperm} was not found.")


@web.middleware
async def tologin(req: web.Request, handler):
    try:
        return await handler(req)
    except web.HTTPUnauthorized as e:
        raise web.HTTPFound("/login", reason=str(e))


# routes
routes = [
    web.static("/static", STATIC_DIR, name="static"),
    web.get("/", index, name="index"),
    web.get("/_base", _base, name="base"),
    web.get("/user", userpage),
    web.get("/login", login_page),
    web.get("/signup", signup_page),
    web.post("/loginp", login),
    web.post("/signupp", signup),
    web.get("/logout", logout),
    web.get(_perm_page_regex("perm"), perm),
    web.get(_perm_page_regex("test"), test_perm),
    web.post("/update_perm", update_perm),
]


# setup views
def setup(app: web.Application):
    app.add_routes(routes)
    app.middlewares.append(tologin)
    mako_setup(app, str(TEMPLATE_DIR))
