import asyncpg
from asyncpg import Record
from asyncpg.pool import Pool
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from __init__ import cred
from contextlib import asynccontextmanager


@asynccontextmanager
async def database_ctx(app: Starlette):
    async with asyncpg.create_pool(**cred, min_size=6, max_size=6) as pool:
        app.state.DB = pool
        yield


async def brands(request: Request) -> JSONResponse:
    connection: Pool = request.app.state.DB
    brand_query = "SELECT brand_id, brand_name FROM brand"
    results: list[Record] = await connection.fetch(brand_query)
    result_as_dict: list[dict] = [dict(brand) for brand in results]
    return JSONResponse(result_as_dict)


app = Starlette(
    routes=[Route("/brands", brands)],
    lifespan=database_ctx,
)
