from pathlib import Path
from typing import Callable, cast

import aiohttp_sse as sse
from aiohttp import web
from aiohttp.typedefs import Handler
from aiohttp_mako import setup as mako_setup
from aiohttp_mako import template as _tmp
from store import UserMsg, get_messages

WORKING_DIR = Path.cwd()
PUBLIC_DIR = WORKING_DIR / "public"
TEMPLATES_DIR = PUBLIC_DIR / "templates"
STATIC_DIR = PUBLIC_DIR / "static"
template = cast(Callable[[str], Callable[..., Handler]], _tmp)


@template("index.mako")
async def index(req: web.Request):
    return {"messages": get_messages(req).messages}


@template("chat.mako")
async def chat(req: web.Request):
    return {"messages": get_messages(req).messages}


async def add_message(req: web.Request):
    data = await req.post()
    manager = get_messages(req)
    sender = data.get("sender", "Anonymous")
    message = data.get("message", None)
    if message is None or not message:
        raise web.HTTPBadRequest(reason="Message Body is Empty | None")
    msg = UserMsg(sender=str(sender), message=str(message))
    await manager.add(msg)
    raise web.HTTPCreated(reason=f"Message {msg} added.")


async def message_sub(req: web.Request):
    async with sse.sse_response(req) as resp:
        ...
    return resp


routes: list[web.AbstractRouteDef] = [
    web.get("/", index),
    web.static("/static", STATIC_DIR, name="static"),
    web.post("/message", add_message, name="add-msg"),
    web.get("/chat", chat, name="chat-page"),
    web.get("/message", message_sub, name="msg-sub"),
]


def setup(app: web.Application):
    mako_setup(app, str(TEMPLATES_DIR))
    app.add_routes(routes)
