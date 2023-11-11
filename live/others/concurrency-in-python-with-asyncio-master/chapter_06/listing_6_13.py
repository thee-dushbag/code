import asyncio
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Value

shared_counter: Value


def init(counter: Value):
    print("Called init with:", counter.value)
    global shared_counter
    shared_counter = counter


def increment():
    with shared_counter:
        shared_counter.value += 1


async def main():
    counter = Value("d", 0)
    with ProcessPoolExecutor(
        max_workers=1, initializer=init, initargs=(counter,)
    ) as pool:
        await asyncio.get_running_loop().run_in_executor(pool, increment)
        print(counter.value)


if __name__ == "__main__":
    asyncio.run(main())
