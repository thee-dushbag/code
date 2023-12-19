import asyncio as aio

counter: int = 0


async def increment():
    global counter
    await aio.sleep(0.01)
    counter += 1


async def main():
    global counter
    for cnt in range(1, 1001):
        tasks = (aio.create_task(increment()) for _ in range(100))
        await aio.gather(*tasks)
        print(f"{cnt}. Counter is {counter}")
        assert counter == 100
        counter = 0


if __name__ == "__main__":
    aio.run(main())
