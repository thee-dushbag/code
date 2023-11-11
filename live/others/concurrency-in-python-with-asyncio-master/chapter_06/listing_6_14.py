import asyncio
import functools
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Value
from typing import Dict, List

from listing_6_8 import merge_dictionaries, partition

map_progress: Value


def init(progress: Value):
    global map_progress
    map_progress = progress


def map_frequencies(chunk: List[str]) -> Dict[str, int]:
    counter = {}
    for line in chunk:
        word, _, count, _ = line.split("\t")
        counter[word] = counter.get(word, 0) + int(count)

    with map_progress:
        map_progress.value += 1

    return counter


async def progress_reporter(total_partitions: int):
    while map_progress.value < total_partitions:
        print(f"Finished {map_progress.value}/{total_partitions} map operations")
        await asyncio.sleep(0.5)


async def main(partiton_size: int):
    global map_progress

    with open("googlebooks-eng-all-1gram-20120701-a", encoding="utf-8") as f:
        contents = f.readlines()
        loop = asyncio.get_running_loop()
        tasks = []
        map_progress = Value("i", 0)

        with ProcessPoolExecutor(
            max_workers=2, initializer=init, initargs=(map_progress,)
        ) as pool:
            total_partitions = len(contents) // partiton_size
            reporter = asyncio.create_task(progress_reporter(total_partitions))

            for chunk in partition(contents, partiton_size):
                tasks.append(loop.run_in_executor(pool, map_frequencies, chunk))

            counters = await asyncio.gather(*tasks)

            await reporter

            final_result = functools.reduce(merge_dictionaries, counters)

            print(f"Aardvark has appeared {final_result.get('Aardvark', 0)} times.")


if __name__ == "__main__":
    asyncio.run(main(partiton_size=60000))
