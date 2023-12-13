from aiohttp import web
from listing_10_4 import getpool, database_ctx


async def favorites(req: web.Request) -> web.Response:
    try:
        user_id = int(req.match_info["id"])
        db = getpool(req)
        favorite_query = "SELECT product_id from user_favorite where user_id = $1"
        result = await db.fetch(favorite_query, user_id)
        if result is None:
            raise web.HTTPNotFound()
        return web.json_response([dict(record) for record in result])
    except ValueError:
        raise web.HTTPBadRequest()


routes = [web.get(r"/users/{id:\d+}/favorites", favorites)]


async def application() -> web.Application:
    app = web.Application()
    app.cleanup_ctx.append(database_ctx)
    app.add_routes(routes)
    return app


if __name__ == "__main__":
    web.run_app(application(), port=8002)
