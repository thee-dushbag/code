import asyncio as aio

from aiohttp import ClientSession as Session
from aiohttp import hdrs
from aiohttp_sse_client.client import EventSource
from yarl import URL

BASEURL = URL("http://localhost:5052")
GRAPHQL = BASEURL / "graphql"


async def main():
    ...


if __name__ == "__main__":
    try:
        aio.run(main())
    except KeyboardInterrupt:
        ...
