import asyncio
from asyncio.events import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import List


def countdown(count_from: int) -> int:
    counter = 0
    print(f"Counting to: {count_from}")
    while counter < count_from:
        counter = counter + 1
    print(f"Done counting to: {count_from}")
    return counter


async def main():
    with ProcessPoolExecutor() as process_pool:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        nums = [10000, 3000, 100000000, 50000, 2200]
        calls: List[partial[int]] = (partial(countdown, num) for num in nums)
        call_coros = [loop.run_in_executor(process_pool, call) for call in calls]

        # for call in calls:
        #     call_coros.append(loop.run_in_executor(process_pool, call))

        for result in asyncio.as_completed(call_coros):
            print(f"\033[92;1mFinished\033[97;1m:\033[0m {await result}")

        # results = await asyncio.gather(*call_coros)
        # print(results)
        # for result in results:
        #     print(result)


if __name__ == "__main__":
    asyncio.run(main())
