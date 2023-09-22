from multiprocessing import Pool, cpu_count, current_process


def say_hello(name: str) -> str:
    process = current_process()
    print(f"Greeting {name} in process: {process.ident}")
    return f"Hi there, {name}"


if __name__ == "__main__":
    process = current_process()
    print(f"main process: {process.ident} | cpu_count: {cpu_count()}")
    with Pool() as process_pool:
        hi_jeff = process_pool.apply_async(say_hello, args=("Jeff",))
        hi_john = process_pool.apply_async(say_hello, args=("John",))
        print(hi_jeff.get())
        print(hi_john.get())
