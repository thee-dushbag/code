from aiohttp import web
from listing_10_4 import getpool, database_ctx

async def carts(request: web.Request) -> web.Response:
    try:
        user_id = int(request.match_info["id"])
        db = getpool(request)
        favorite_query = "SELECT product_id from user_cart where user_id = $1"
        result = await db.fetch(favorite_query, user_id)
        if result is None:
            raise web.HTTPNotFound()
        return web.json_response([dict(record) for record in result])
    except Exception:
        raise web.HTTPBadRequest()


routes = [web.get(r"/users/{id:\d+}/cart", carts)]


async def application() -> web.Application:
    app = web.Application()
    app.cleanup_ctx.append(database_ctx)
    app.add_routes(routes)
    return app


if __name__ == "__main__":
    web.run_app(application(), port=8003)
