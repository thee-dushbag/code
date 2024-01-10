import asyncio, types


@types.coroutine
def coroutine():
    print("Sleeping!")
    yield from asyncio.sleep(1)
    print("Finished!")


if __name__ == "__main__":
    asyncio.run(coroutine())  # type: ignore
