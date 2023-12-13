from aiohttp.web_app import Application
from aiohttp.web_request import Request
from __init__ import cred
import asyncpg

DB_KEY = "database"

async def database_ctx(app: Application):
    async with asyncpg.create_pool(**cred, min_size=6, max_size=6) as pool:
        app[DB_KEY] = pool
        yield

def getapp_pool(app: Application) -> asyncpg.Pool:
    if pool := app.get(DB_KEY): return pool
    raise Exception("Database Context not setup, call app.cleanup_ctx.append(database_ctx)")

def getpool(req: Request) -> asyncpg.Pool:
    return getapp_pool(req.app)
