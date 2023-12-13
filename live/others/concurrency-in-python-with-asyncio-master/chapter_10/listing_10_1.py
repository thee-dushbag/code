from aiohttp import web
import asyncio, random


async def get_inventory(req: web.Request) -> web.Response:
    delay: float = random.randint(0, 20) / 10
    await asyncio.sleep(delay)
    inventory: int = random.randint(0, 100)
    return web.json_response({"inventory": inventory})


routes = [web.get("/products/{id}/inventory", get_inventory)]


async def application():
    app = web.Application()
    app.add_routes(routes)
    return app


if __name__ == "__main__":
    web.run_app(application(), port=8001)
