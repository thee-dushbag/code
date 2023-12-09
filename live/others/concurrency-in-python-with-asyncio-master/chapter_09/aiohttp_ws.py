from aiohttp import web
import userconn as us


async def htmlpage(req: web.Request):
    with open("./listing_9_10.html") as file:
        html_content = file.read()
    return web.Response(text=html_content, content_type="text/html", status=200)


async def counter(req: web.Request) -> web.WebSocketResponse:
    client = web.WebSocketResponse(timeout=1, heartbeat=2)
    await client.prepare(req)
    async with us.getclients(req).context(client):
        async for msg in client:
            print(f"[{hex(id(client))}] Received: {msg.data}")
    return client


routes = [web.get("/", htmlpage), web.get("/counter", counter)]


async def application():
    app = web.Application()
    us.setup(app)
    app.add_routes(routes)
    return app


if __name__ == "__main__":
    web.run_app(application())
