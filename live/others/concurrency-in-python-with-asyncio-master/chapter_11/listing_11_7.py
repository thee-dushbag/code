import asyncio as aio
from aiohttp import ClientSession

URL = "https://www.example.com"


async def get_url(url: str, session: ClientSession, semaphore: aio.Semaphore):
    print("Waiting to acquire semaphore...")
    async with semaphore:
        print("Acquired semaphore, requesting...")
        response = await session.get(url)
        print("Finished requesting")
        return response.status


async def main():
    semaphore = aio.Semaphore(10)
    async with ClientSession() as session:
        tasks = (get_url(URL, session, semaphore) for _ in range(1000))
        await aio.gather(*tasks)


if __name__ == "__main__":
    aio.run(main())
