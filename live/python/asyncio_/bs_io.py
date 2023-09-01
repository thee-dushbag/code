import asyncio as aio
from time import sleep
from uvloop import install
from threading import current_thread

def say_what(sym: str):
    counter = 0
    try:
        while True:
            state = yield counter
            print(f"[{sym}]: Counter at: {counter} with state: {state}")
            counter += 1
    except ZeroDivisionError:
        print(f"Recieved: ZeroDivisionError")
        t = say_what(sym)
        t.send(None)
        yield from t
    except TypeError:
        print(f"Recieved: TypeError")
    except AttributeError:
        print(f"Recieved: AttributeError")



def which_thread(sym: str):
    thread = current_thread()
    tid = thread.native_id
    name = thread.name
    print(f"[{sym}]: You are in: {name} thread with id {tid}")

async def run_in_executor(executor, func, *args, **kwargs):
    loop = aio.get_running_loop()
    task = loop.run_in_executor(executor, func, *args, **kwargs)
    return await task

install()
from typing import Any, Sequence

def blocking_sleep(delay: float, result: Any):
    print(f"Blocking for: {delay}")
    sleep(delay)
    which_thread("blocking_sleep")
    print(f"Returning: {result}")
    return result

async def say_hi(name: str, delay: float=1) -> None:
    print(f"Hello {name}, how was your day?")
    which_thread("say_hi")
    await aio.sleep(delay)
    print(f"Greeted: {name}!")

async def main(argv: Sequence[str]) -> None:
    # which_thread("main")
    # await say_hi("Simon Nganga", 0)
    # msg = await run_in_executor(None, blocking_sleep, 3, "Hello World")
    # print(f"msg: {msg}")
    gen = say_what("test")
    gen.send(None)
    try:
        for i in range(50):
            print(f"main received: {i}")
            gen.send(i * i) # type: ignore
            if i % 5 == 0:
                gen.throw(ZeroDivisionError)
    except StopIteration:
        pass


if __name__ == '__main__':
    from sys import argv
    aio.run(main(argv[1:]))