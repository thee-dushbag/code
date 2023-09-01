from aiohttp_sse_client.client import EventSource, ClientConnectionError
import asyncio as aio
from datetime import timedelta
from time import time, asctime, localtime
from yarl import URL

rtime = timedelta(seconds=5)

HOST, PORT = "localhost", 5052
BASE_URL = URL(f"http://{HOST}:{PORT}")
url = BASE_URL / "sse"


def caller(message):
    def other(*a):
        current = time()
        local = localtime(current)
        stime = asctime(local)
        print(f"[{stime}]: Operation: {message}")

    return other


def on_msg(msg):
    print(f"New Message: {msg.data!r}")


async def main():
    try:
        async with EventSource(str(url)) as msgs:
            async for msg in msgs:
                on_msg(msg)
    except (ClientConnectionError, aio.CancelledError, KeyboardInterrupt) as e:
        print(f"ERROR: {e}")


aio.run(main())
