from aiohttp import ClientSession, ServerDisconnectedError
import asyncio

HOST = "localhost"  # Default aiohttp server host
PORT = 8080  # Default aiohttp server port
BASE_URL = f"http://{HOST}:{PORT}"


async def place_order(session: ClientSession):
    async with session.get("/order") as resp:
        print(await resp.text())


async def stress():
    async with ClientSession(BASE_URL) as session:
        orders = (place_order(session) for _ in range(100))
        await asyncio.gather(*orders)


if __name__ == "__main__":
    try:
        asyncio.run(stress())
    except: ... 
