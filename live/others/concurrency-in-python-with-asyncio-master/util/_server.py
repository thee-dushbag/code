import asyncio as aio  # , rich

from aiohttp import hdrs, web
# from mpack.aiohttp_helpers import cors_setup, dev_setup


async def index(req: web.Request):
    await aio.sleep(2)
    return web.Response(text="Hello World")


async def sleeper(req: web.Request):
    delay = float(req.match_info.get("time") or 0.5)
    resp = web.Response(text=f"Sleeping for {delay} second(s).")
    return await aio.sleep(delay, resp)


routes = [
    web.get("/delay/{time:[0-9]+(.[0-9]+)?}", sleeper),
    web.route(hdrs.METH_ANY, "/", index),
    web.get("/delay", sleeper),
]


@web.middleware
async def log_client_data(req: web.Request, handler):
    # rich.print(dict(req.headers))
    return await handler(req)


async def application():
    app = web.Application()
    app.middlewares.append(log_client_data)
    app.add_routes(routes)
    # dev_setup(app)
    # cors_setup(app)
    return app


def run():
    web.run_app(application(), host="localhost", port=5052)


if __name__ == "__main__":
    run()
