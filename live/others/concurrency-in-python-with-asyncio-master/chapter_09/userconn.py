from aiohttp import web
from aiohttp.web_ws import WebSocketResponse
import asyncio as aio

APP_KEY = "websocket.clients.connected"


class ConnectedClients(list[web.WebSocketResponse]):
    async def remove(self, client: web.WebSocketResponse) -> None:
        try:
            super().remove(client)
            await self.update_count()
        except ValueError:
            ...

    async def send_count(self, client: web.WebSocketResponse):
        try:
            connected_count = str(len(self))
            await client.send_str(connected_count)
        except Exception:
            await self.remove(client)

    async def update_count(self) -> None:
        if not self:
            return
        tasks = (self.send_count(c) for c in self)
        await aio.gather(*tasks)

    async def append(self, client: WebSocketResponse) -> None:
        super().append(client)
        await self.update_count()

    def context(self, client: web.WebSocketResponse) -> "_ConnectedClientContext":
        return _ConnectedClientContext(client, self)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        ...


class _ConnectedClientContext:
    def __init__(self, client: web.WebSocketResponse, conns: ConnectedClients) -> None:
        self.id = hex(id(client))
        self.connected = conns
        self.client = client

    async def __aenter__(self):
        print(f"Client: {self.id} connected")
        await self.connected.append(self.client)
        return self.client

    async def __aexit__(self, *_):
        print(f"Client: {self.id} disconnected")
        await self.connected.remove(self.client)


async def connected_ctx(app: web.Application):
    async with ConnectedClients() as connected_clients:
        app[APP_KEY] = connected_clients
        yield


def getappclients(app: web.Application) -> ConnectedClients:
    if APP_KEY in app:
        return app[APP_KEY]
    raise RuntimeError("connected clients context was not initialized")


def getclients(req: web.Request) -> ConnectedClients:
    return getappclients(req.app)


def setup(app: web.Application):
    app.cleanup_ctx.append(connected_ctx)
