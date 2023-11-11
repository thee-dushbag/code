import asyncio
import concurrent.futures
import functools
import time, json
from collections import defaultdict
from typing import Dict, Generator, List


def partition(data: List, chunk_size: int) -> Generator[List, None, None]:
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]


def map_frequencies(chunk: List[str]) -> Dict[str, int]:
    counter = defaultdict(lambda: 0)
    for line in chunk:
        word, _, count, _ = line.split("\t")
        counter[word] += int(count)
    return dict(counter)


def merge_dictionaries(first: Dict[str, int], second: Dict[str, int]) -> Dict[str, int]:
    for word, count in second.items():
        first[word] = first.get(word, 0) + count
    return first


async def main(partition_size: int):
    with open("googlebooks-eng-all-1gram-20120701-a", encoding="utf-8") as f:
        contents = f.readlines()
        loop = asyncio.get_running_loop()
        start = time.time()
        with concurrent.futures.ProcessPoolExecutor() as pool:
            tasks = [
                loop.run_in_executor(pool, functools.partial(map_frequencies, chunk))
                for chunk in partition(contents, partition_size)
            ]

            intermediate_results = await asyncio.gather(*tasks)
            final_result = functools.reduce(merge_dictionaries, intermediate_results)

            end = time.time()

            print(f"Aardvark has appeared {final_result['Aardvark']} times.")
            print(f"MapReduce took: {(end - start):.4f} seconds")
    with open('n-gram2.json', 'w') as f:
        json.dump(dict(final_result), f, indent=2)


if __name__ == "__main__":
    asyncio.run(main(partition_size=60000))
