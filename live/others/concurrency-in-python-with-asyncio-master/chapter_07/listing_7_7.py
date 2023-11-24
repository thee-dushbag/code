import asyncio

import requests
from util import async_timed


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


@async_timed()
async def main():
    url = "https://www.example.com"
    tasks = (asyncio.to_thread(get_status_code, url) for _ in range(20))
    results = await asyncio.gather(*tasks)
    print(results)


asyncio.run(main())
