import asyncpg
from aiohttp import web
from __init__ import cred

DB_KEY = "database"


async def database_ctx(app: web.Application):
    async with asyncpg.create_pool(**cred, min_size=6, max_size=6) as pool:
        app[DB_KEY] = pool
        yield


async def get_product(request: web.Request) -> web.Response:
    str_id = request.match_info["id"]  # A
    product_id = int(str_id)

    query = """
        SELECT
        product_id,
        product_name,
        brand_id
        FROM product
        WHERE product_id = $1
        """

    connection: asyncpg.Pool = request.app[DB_KEY]
    result: asyncpg.Record = await connection.fetchrow(query, product_id)  # B

    if result is None:  # C
        raise web.HTTPNotFound
    return web.json_response(dict(result))


routes = [web.get(r"/products/{id:\d+}", get_product)]


async def application():
    app = web.Application()
    app.cleanup_ctx.append(database_ctx)
    app.add_routes(routes)
    return app


if __name__ == "__main__":
    web.run_app(application())
