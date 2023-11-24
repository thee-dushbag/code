import asyncio

import requests
from util import async_timed


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


@async_timed()
async def main():
    loop = asyncio.get_running_loop()
    url = "https://www.example.com"
    tasks = (loop.run_in_executor(None, get_status_code, url) for _ in range(1000))
    results = await asyncio.gather(*tasks)
    print(results)


asyncio.run(main())
