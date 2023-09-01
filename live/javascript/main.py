from httpx import AsyncClient
from aiohttp.client import ClientSession
from typing import Sequence
from mpack.timer import TimeitResult, timer
import asyncio as aio
from mpack import timer as _t
from mpack import print
from yarl import URL
from requests import Session

_t.FUNCTION_CALL_STR = '{function_name:15}'
HOST, PORT = 'localhost', 5052
BASE_URL = URL(f'http://{HOST}:{PORT}')
INDEX_URL = BASE_URL.with_path('')

@timer
async def requestsmain() -> str:
    loop = aio.get_event_loop()
    with Session() as client:
        # resp = client.get(str(INDEX_URL))
        resp = await loop.run_in_executor(None, client.get, str(INDEX_URL))
    return resp.text

@timer
async def httpxmain() -> str:
    async with AsyncClient(base_url=str(BASE_URL)) as client:
        resp = await client.get(str(INDEX_URL))
    return resp.text

@timer
async def aiohttpmain() -> str:
    async with ClientSession(BASE_URL) as client:
        async with client.get(INDEX_URL.path) as resp:
            return await resp.text()

@timer
async def main(argv: Sequence[str]) -> None:
    tasks = requestsmain, httpxmain, aiohttpmain
    coros = (task() for task in tasks)
    results: list[TimeitResult[str]] = await aio.gather(*coros)
    print(*results, sep='\n')

if __name__ == '__main__':
    from sys import argv #type:ignore
    result = aio.run(main(argv[1:]))
    print(result)