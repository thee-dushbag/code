from aiohttp import web
from listing_9_2 import database_ctx

DB_KEY = "database"


async def create_product(request: web.Request) -> web.Response:
    PRODUCT_NAME = "product_name"
    BRAND_ID = "brand_id"

    if not request.can_read_body:
        raise web.HTTPBadRequest()

    body = await request.json()

    if PRODUCT_NAME in body and BRAND_ID in body:
        db = request.app[DB_KEY]
        await db.execute(
            """INSERT INTO product(product_id,
                    product_name, brand_id)
                    VALUES (DEFAULT, $1, $2)""",
            body[PRODUCT_NAME],
            int(body[BRAND_ID]),
        )
        return web.Response(status=201)
    raise web.HTTPBadRequest


routes = [web.post(r"/products", create_product)]


async def application():
    app = web.Application()
    app.cleanup_ctx.append(database_ctx)
    app.add_routes(routes)
    return app


if __name__ == "__main__":
    web.run_app(application())
