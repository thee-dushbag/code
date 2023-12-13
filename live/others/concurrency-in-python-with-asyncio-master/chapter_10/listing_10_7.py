from aiohttp import web
from listing_10_4 import getpool, database_ctx


async def products(request: web.Request) -> web.Response:
    db = getpool(request)
    product_query = "SELECT product_id, product_name FROM product"
    result = await db.fetch(product_query)
    return web.json_response([dict(record) for record in result])


routes = [web.get("/products", products)]


async def application() -> web.Application:
    app = web.Application()
    app.cleanup_ctx.append(database_ctx)
    app.add_routes(routes)
    return app


if __name__ == "__main__":
    web.run_app(application(), port=8000)
