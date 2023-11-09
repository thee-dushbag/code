import asyncio as aio


def hello(name: str) -> None:
    print(f"Hello {name}?")


async def main():
    loop = aio.get_running_loop()
    loop.call_later(3, hello, "Simon Nganga")
    loop.time()
    for _ in range(5):
        print(f"Waiting: {_}")
        await aio.sleep(1)


if __name__ == '__main__':
    aio.run(main()) 