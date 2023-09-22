import asyncio as aio
from time import sleep
from typing import Sequence

from bs4 import BeautifulSoup
from faker import Faker
from httpx import AsyncClient, Client
from mpack.timer import TimeitConfig, timer_conf

GREET_URL_SITE = "http://localhost:4321"
CSRF_TOKEN = "ThisIsMyCRSFTOKEN"
config = TimeitConfig(
    function_call_str="{function_name!r}", taken_time_str="[{target}]: {lapse} seconds."
)


def get_greet_sync(name: str, delay: float = 0.8) -> str:
    with Client(base_url=GREET_URL_SITE, follow_redirects=True) as client:
        greetings = client.post("/greet_post", data=dict(name=name))
        sleep(delay)
    if greetings.status_code == 200:
        soup = BeautifulSoup(greetings.content.decode(), "lxml")
        return soup.html.body.div.h3.center.text  # type: ignore
    return f"[SYNC]: Error greeting: {name}"


async def get_greet_async(name: str, delay: float = 0.8) -> str:
    async with AsyncClient(base_url=GREET_URL_SITE, follow_redirects=True) as client:
        greetings = await client.post(
            "/greet_post", data=dict(name=name, csrfmiddlewaretoken=CSRF_TOKEN)
        )
        await aio.sleep(delay)
    if greetings.status_code == 200:
        soup = BeautifulSoup(greetings.content.decode(), "lxml")
        return soup.html.body.div.h3.center.text  # type: ignore
    return f"[ASYNC]: Error greeting: {name}"


@timer_conf(config)
def greet_names_sync(names: list[str], delay: float = 0.8) -> list[str]:
    return [get_greet_sync(name, delay) for name in names]


@timer_conf(config)
async def greet_names_async(names: list[str], delay: float = 0.8) -> list[str]:
    return await aio.gather(*(get_greet_async(name, delay) for name in names))


async def main(argv: Sequence[str]) -> None:
    #   fake, delay = Faker(), .5
    #   names = [fake.name() for _ in range(100)]
    #    loop = aio.get_running_loop()
    #    sync_task = loop.run_in_executor(None, greet_names_sync, names, delay)
    #    async_task = greet_names_async(names, delay)
    # greetings_sync = greet_names_sync(names, delay)
    greetings_async = await greet_names_async(argv, 0)
    #    greetings_sync, greetings_async = await aio.gather(sync_task, async_task)
    #   print(f'Greeting SYNC:\n{greetings_sync.result}')
    #   print(f'Greeting ASYNC:\n{greetings_async.result}')
    #   print(greetings_async, greetings_sync, sep='\n')
    #   assert greetings_async.result == greetings_sync.result, "Greetings are not the same"
    for cnt, greeting in enumerate(greetings_async.result):
        print(f"{cnt + 1}: {greeting}")
    print(greetings_async)


if __name__ == "__main__":
    from sys import argv

    aio.run(main(argv[1:]))
