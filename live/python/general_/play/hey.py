import asyncio as aio
from threading import current_thread

from mpack import print


async def say_hi(name: str) -> str:
    tid = current_thread().ident
    print(f"[{tid}]: Hello {name.title()}, how was your day?")
    await aio.sleep(2)


async def say_hi_to(names: list[str]):
    tasks = (say_hi(n) for n in names)
    await aio.gather(*tasks)


async def main(names: list[str]) -> None:
    opt, *names = names
    if not names:
        print("Please Enter Names on the CommandLine")
    elif opt == "sync":
        for name in names:
            await say_hi(name)
    elif opt == "async":
        await say_hi_to(names)
    else:
        print(f"Unknown option: {opt} => [sync | async]")


def print_to(start, stop, step=1):
    for i in range(start, stop, step):
        print(f"i : {i}")


if __name__ == "__main__":
    from sys import argv

    names = list(name for name in argv[1:] if name)
    aio.run(main(names))
