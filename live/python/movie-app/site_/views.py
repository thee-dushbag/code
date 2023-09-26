import asyncio as aio
import re

import config as cfg
from aiohttp import web
from aiohttp_mako import setup as mako_setup
from movies import Movies
from mpack.aiohttp_helpers.mako_ import template_handler

SOURCE_PAT = re.compile(r"/source/(?P<src>[a-z]+)/(?P<file>.*$)")
app_movies: Movies
TOTAL: int
index = template_handler("home.mako")
movies = template_handler("movies.mako")


async def movies_api(req: web.Request):
    offset = req.query.get("offset", "")
    size = req.query.get("size", "")
    start_idx = int(offset) if offset.isnumeric() else 0
    end_idx = (int(size) if size.isnumeric() else 10) + start_idx
    payload = dict(
        movies=[m.json_min() for m in app_movies.movies[start_idx:end_idx]],
        total=TOTAL,
    )
    return web.json_response(payload)


async def shutter(delay: int):
    loop = aio.get_running_loop()
    loop.call_later(delay, exit)


async def shut(req: web.Request):
    delay = int(req.match_info.get("delay", None) or 10)
    resp = web.Response(body=f"Shutting down in {delay} second(s)...")
    await shutter(delay)
    return resp


routes = [
    web.get("/", index),
    web.get("/movies", movies),
    web.get("/movies_api", movies_api),
    web.static("/source/movie", cfg.MOVIE_DIR),
    web.static("/source/preview", cfg.PREVIEW_DIR),
    web.static("/source/thumbnail", cfg.THUMBNAIL_DIR),
    web.static("/static", cfg.STATIC_DIR),
    web.get("/shut", shut),
    web.get(r"/shut/{delay:\d+}", shut),
]


@web.middleware
async def static_not_found(req: web.Request, handler):
    if source := re.fullmatch(SOURCE_PAT, req.url.path):
        try:
            return await handler(req)
        except web.HTTPNotFound as e:
            source_type = source.group("src")
            file, src = source.group("file"), None
            reason = f"The requested file {file!r} was not found."
            if source_type == "thumbnail":
                src, file = source_type, cfg.NO_THUMBNAIL.name
            elif source_type == "preview":
                src, file = source_type, cfg.NO_PREVIEW.name
            raise web.HTTPFound(f"/source/{src}/{file}", reason=reason) if src else e
    return await handler(req)


@web.middleware
async def favicon_ico(req: web.Request, handler):
    if req.url.path == "/favicon.ico":
        raise web.HTTPFound("/static/favicon.128.ico")
    return await handler(req)


def setup(app: web.Application, mov: Movies):
    global app_movies, TOTAL
    TOTAL = len(mov.movies)
    app_movies = mov
    app.middlewares.extend([static_not_found, favicon_ico])
    app.add_routes(routes)
    mako_setup(app, str(cfg.TEMPLATES_DIR))
