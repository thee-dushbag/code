import asyncio as aio
from pathlib import Path
from typing import Sequence

from aiofiles import open as aopen
from bs4 import BeautifulSoup as Soup
from httpx import AsyncClient, Client
from mpack.timer import TimeitConfig, timer, timer_conf
from yarl import URL

DOWNLOAD_CONFIG = TimeitConfig(function_call_str="{function_name}")  # type:ignore
HOST, PORT = "192.168.0.100", 5052
BASE_URL = URL(f"http://{HOST}:{PORT}")
MOVIE_BIN = BASE_URL.with_path("movie")
MOVIE_PAGE = BASE_URL.with_path("movie_page")
DOWNLOAD_DIR = Path(__file__).parent / "movies"
CHUNK_SIZE = None  # 5120

if not DOWNLOAD_DIR.exists():
    if DOWNLOAD_DIR.is_dir():
        for path in DOWNLOAD_DIR.iterdir():
            path.unlink()
        DOWNLOAD_DIR.rmdir()
    DOWNLOAD_DIR.mkdir()

if not DOWNLOAD_DIR.is_dir():
    raise NotADirectoryError(str(DOWNLOAD_DIR))


async def get_movie_list():
    async with AsyncClient(base_url=str(BASE_URL)) as client:
        page = await client.get(MOVIE_PAGE.path)
    soup = Soup(page.text, "lxml")
    links = soup.find_all("div", attrs={"class", "movie_link"})
    return [link.attrs["movie_name"] for link in links]


@timer
async def async_download_movie(movie_name: str):
    print(f"Downloading: {movie_name}")
    async with AsyncClient(base_url=str(BASE_URL)) as client:
        async with client.stream("get", str(MOVIE_BIN / movie_name)) as movie_stream:
            async with aopen(str(DOWNLOAD_DIR / movie_name), "wb") as file:
                # with open(str(DOWNLOAD_DIR / movie_name), 'wb') as file:
                async for content in movie_stream.aiter_bytes(CHUNK_SIZE):
                    await file.write(content)
                    # file.write(content)
    print(f"Finished Download: {file.name}")


@timer_conf(DOWNLOAD_CONFIG)
async def async_download_movies(movie_names: Sequence[str]):
    tasks = (async_download_movie(movie_name) for movie_name in movie_names)
    return await aio.gather(*tasks, return_exceptions=True)


@timer
def sync_download_movie(movie_name: str):
    print(f"Downloading: {movie_name}")
    with Client(base_url=str(BASE_URL)) as client:
        with client.stream("get", str(MOVIE_BIN / movie_name)) as movie_stream:
            with open(str(DOWNLOAD_DIR / movie_name), "wb") as file:
                for content in movie_stream.iter_bytes(CHUNK_SIZE):
                    file.write(content)
    print(f"Finished Download: {file.name}")


@timer_conf(DOWNLOAD_CONFIG)
def sync_download_movies(movie_names: Sequence[str]):
    return [sync_download_movie(movie_name) for movie_name in movie_names]


async def main(argv: Sequence[str]) -> None:
    movs = await get_movie_list()
    timeit_results = await async_download_movies(movs)
    # timeit_results = sync_download_movies(movs)
    for result in timeit_results.result:
        print(result)
    print(timeit_results)


if __name__ == "__main__":
    from sys import argv

    aio.run(main(argv[1:]))
