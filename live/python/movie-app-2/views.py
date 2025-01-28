import typing as ty

import config as cfg
import movies as mov
from aiohttp import typedefs, web
from mako_helpers import template_handler


def _raise(attr: str, valtype: type, value: ty.Any = None):
    raise web.HTTPBadRequest(
        reason=f"Invalid value for {attr}, expected {valtype.__name__} but found {value}"
    )


async def movies(req: web.Request):
    soffset = req.query.get("offset", "0")
    slimit = req.query.get("limit", "5")
    if not soffset.isnumeric():
        _raise("offset", int)
    if not slimit.isnumeric():
        _raise("limit", int)
    offset, limit = int(soffset), int(slimit)
    m = mov.movies(req)
    movies = dict(movies=m.partition(offset, limit).json(), total=m.total)
    return web.json_response(movies)


async def movie(req: web.Request):
    movies = mov.movies(req)
    movie_id = int(req.match_info.get("movie_id", 0))
    try:
        movie = movies.movies[movie_id]
        return web.json_response(movie.json())
    except IndexError:
        raise web.HTTPBadRequest(reason=f"No movie with id {movie_id}")


async def refresh(req: web.Request):
    movies = mov.movies(req)
    try:
        sortorder = req.query["sortby"]
        order = mov.Order(sortorder)
        movies.sort_movies(order)
        movies.order = order
    except KeyError:
        pass
    try:
        movies.set_movies()
        if req.query["load"].lower() in ("y", "t", "yes", "true"):
            cfg.generate_previews(cfg.config(req))
            cfg.generate_thumbnails(cfg.config(req))
    except KeyError:
        pass
    return web.HTTPTemporaryRedirect("/")


# Templates
movies_page = template_handler("movies.mako")
home_page = template_handler(
    "home.mako", lambda r: dict(movies=mov.movies(r), orders=mov.Order.orders())
)

routes: list[web.AbstractRouteDef] = [
    web.get("/", home_page),
    web.get("/movies", movies_page),
    web.static("/static", cfg.STATIC_DIR),
    web.static("/public", cfg.PUBLIC_DIR),
    web.get("/api/movies", movies, name="movies_api"),
    web.get("/api/refresh", refresh, name="refresh_api"),
    web.get(r"/api/movie/{movie_id:\d+}", movie, name="movie"),
    web.static("/source", cfg.RESOURCE_DIR, follow_symlinks=True),
]


def setup(app: web.Application):
    app.add_routes(routes)
