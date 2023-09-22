from functools import partial
from io import StringIO

from aiohttp import hdrs, web
from basicauth import decode, encode


async def add_path(req, cur, handler):
    def create_new():
        print(f"Creating new path in: {cur}")
        return list()

    # paths = req.setdefault('path', create_new())
    paths = req.get("path", create_new)
    if paths is create_new:
        req["path"] = paths = paths()
    paths.append([cur, handler])


@web.middleware
async def page_404(req, handler):
    await add_path(req, page_404, handler)
    try:
        return await handler(req)
    except web.HTTPClientError as e:
        resp = web.Response(status=404, content_type="text/html")
        resp.text = f"<h1><center><b>Path Not Found: {e.reason}</b></center></h1>"
        return resp


@web.middleware
async def mid_one(req: web.Request, handler):
    await add_path(req, mid_one, handler)
    resp = await handler(req)
    if hdrs.AUTHORIZATION not in req.headers:
        resp.text += "\nYou Did Not Authnticate"
    else:
        auth = req.headers.get(hdrs.AUTHORIZATION)
        username, password = decode(auth)
        resp.text += f"\nYou Authenticated as: {username=} {password=}"
    return resp


@web.middleware
async def mid_two(req: web.Request, handler):
    await add_path(req, mid_two, handler)
    print(f"[mid_two]: Received: {handler} with {req}")
    resp = await handler(req)
    return resp


@web.middleware
async def print_mids(req: web.Request, handler):
    await add_path(req, print_mids, handler)
    file = StringIO()
    p = partial(print, file=file)
    p(f"Middlewares: [{handler}, {req}]")
    for index, mid in enumerate(req.app.middlewares, start=1):
        p(f"\t{index}: {mid.__name__} => {mid!s}")
    resp: web.Response = await handler(req)
    p(f"\n\nOriginal Response: {resp.text!r} {resp.content_type}")
    p("Response handling path route:")
    for index, (cur, han) in enumerate(req.setdefault("path", []), start=1):
        p(f"\t{index}. {cur} -> {han}")
    text = file.getvalue()
    print(text)
    return web.Response(text=text)


def setup(app: web.Application):
    mids = print_mids, mid_one, mid_two, page_404
    app.middlewares.extend(mids)
