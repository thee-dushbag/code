from datetime import datetime
from aiohttp import web
from rich import print


async def time(req: web.Request) -> web.Response:
    today = datetime.today()
    print(dict(req.headers))
    result = dict(
        month=today.month,
        day=today.day,
        year=today.year,
        time=str(today.time())
    )
    return web.json_response(result)  # B


routes = [web.get("/time", time)]


async def application():
    app = web.Application()  # C
    app.add_routes(routes)
    return app


if __name__ == "__main__":
    web.run_app(application())
