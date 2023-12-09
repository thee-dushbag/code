import asyncio

from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.routing import WebSocketRoute, Route
from starlette.websockets import WebSocket
from starlette.responses import HTMLResponse
from starlette.requests import Request


class UserCounter(WebSocketEndpoint):
    encoding = "text"
    connected_clients: list[WebSocket] = []

    async def on_connect(self, websocket: WebSocket):  # A
        await websocket.accept()
        self.connected_clients.append(websocket)
        await self._send_count()

    async def on_disconnect(self, websocket: WebSocket, close_code: int):  # B
        self.connected_clients.remove(websocket)
        await self._send_count()

    async def on_receive(self, websocket: WebSocket, data):
        pass

    async def _send_count(self):  # C
        if not self.connected_clients:
            return
        count_str = str(len(self.connected_clients))
        task_to_socket = {
            asyncio.create_task(websocket.send_text(count_str)): websocket
            for websocket in self.connected_clients
        }

        done, _ = await asyncio.wait(task_to_socket)

        for task in done:
            if task.exception() is not None:
                if task_to_socket[task] in self.connected_clients:
                    self.connected_clients.remove(task_to_socket[task])


async def htmlpage(request: Request) -> HTMLResponse:
    with open("./listing_9_10.html") as file:
        return HTMLResponse(file.read())


app = Starlette(routes=[WebSocketRoute("/counter", UserCounter), Route("/", htmlpage)])
