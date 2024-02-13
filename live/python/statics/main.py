import json, uvloop
from os import getenv
from pathlib import Path
from typing import Any

from aiohttp import hdrs, web
from faker import Faker
from mpack.aiohttp_helpers import cors_setup, dev_setup

CUR_DIR = Path(__file__).parent
STATIC_PATH = CUR_DIR / "static"
FONTS_DIR = Path.home() / ".local" / "share" / "fonts"
if not FONTS_DIR.exists():
    FONTS_DIR.mkdir()
fake = Faker()


async def faker_gen(req: web.Request):
    kwargs: dict[str, Any] = dict(req.query)
    args = ()
    try:
        data = {}
        if req.method.lower() != hdrs.METH_GET.lower():
            data = await req.json()
        else:
            try:
                data = json.loads(str(await req.text()))
            except Exception:
                pass
            if "kwargs" in data:
                kwargs = {**kwargs, **data["kwargs"]}
            if "args" in data:
                args = (*args, *data["args"])
    except Exception:
        raise web.HTTPBadRequest(
            reason=f"Failed to retrieve args and kwargs from request json"
        )
    for key, value in kwargs.items():
        if type(value) in [bytes, str, bytearray, memoryview]:
            if value.isnumeric():
                kwargs[key] = int(value)
    attr = req.match_info.get("attr", "")
    obj = getattr(fake, attr, None)
    if obj is None:
        raise web.HTTPBadRequest(reason=f"Target {attr} was not found.")
    try:
        result = obj
        if callable(obj):
            result = obj(*args, **kwargs)
        extra = {"found": str(obj), "kwargs": kwargs, "args": args, "url": str(req.url)}
        if type(result) in [bytes, bytearray]:
            resp = web.Response(
                body=result, headers={"Faker-Result": json.dumps(extra)}
            )
            return resp
        return web.json_response({"result": result, **extra})
    except Exception:
        raise web.HTTPClientError(reason=f"Error Calling object: {obj}")


async def image_short(req: web.Request):
    width = int(req.query.get("width", 256))
    height = int(req.query.get("height", 256))
    format_ = str(req.query.get("format", "png"))
    kwargs = {"size": (width, height), "image_format": format_}
    return web.Response(
        body=fake.image(**kwargs),
        headers={"Faker-Result": json.dumps({"kwargs": kwargs})},
    )


routes = [
    web.static("/static", STATIC_PATH, name="static", show_index=True),
    web.static("/fonts", FONTS_DIR, name="fonts", show_index=True),
    web.route(hdrs.METH_ANY, r"/faker/{attr}", faker_gen, name="faker"),
    web.get("/image", image_short, name="image"),
]


async def app_factory():
    app = web.Application()
    app.add_routes(routes)
    cors_setup(app)
    dev_setup(app)
    return app


if __name__ == "__main__":
    HOST = getenv("STATICS_HOST")
    PORT = int(getenv("STATICS_PORT") or 9944)
    loop = uvloop.new_event_loop()
    web.run_app(app_factory(), host=HOST, port=PORT, loop=loop)
