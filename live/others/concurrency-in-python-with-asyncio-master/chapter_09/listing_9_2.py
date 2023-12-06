import asyncpg
from aiohttp import web
from __init__ import cred

DB_KEY = "database"


async def database_ctx(app: web.Application):
    async with asyncpg.create_pool(**cred, min_size=6, max_size=6) as pool:
        app[DB_KEY] = pool
        yield


async def brands(request: web.Request) -> web.Response:  # C
    connection: asyncpg.Pool = request.app[DB_KEY]
    brand_query = "SELECT brand_id, brand_name FROM brand"
    results: list[asyncpg.Record] = await connection.fetch(brand_query)
    result_as_dict: list[dict] = [dict(brand) for brand in results]
    return web.json_response(result_as_dict)


routes = [web.get("/brands", brands)]


async def application():
    app = web.Application()
    app.cleanup_ctx.append(database_ctx)
    app.add_routes(routes)
    return app


if __name__ == "__main__":
    web.run_app(application())
