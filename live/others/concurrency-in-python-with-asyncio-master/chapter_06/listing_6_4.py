import time
from concurrent.futures import ProcessPoolExecutor


def count(count_to: int) -> int:
    start = time.time()
    counter = 0
    while counter < count_to:
        counter = counter + 1
    end = time.time()
    print(f'Finished counting to {count_to} in {end - start} seconds')
    return counter


if __name__ == "__main__":
    with ProcessPoolExecutor() as process_pool: # RAII
        # + __enter__ -> Aqqcuire
        # + __exit__  -> Release
        numbers = 1, 3, 100000, 5, 22
        for result in process_pool.map(count, numbers):
            print(result)
