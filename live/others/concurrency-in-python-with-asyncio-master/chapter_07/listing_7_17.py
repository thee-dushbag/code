import asyncio
# import functools
import hashlib
import os
import random
import string
# from concurrent.futures.thread import ThreadPoolExecutor

from util import async_timed

ascii_lowercase = string.ascii_lowercase.encode()

def random_password(length: int) -> bytes:
    elements = random.choices(ascii_lowercase, k=length)
    return b"".join(bytes(e) for e in elements)

passwords = (random_password(10) for _ in range(10000))


def hash_password(password: bytes) -> str:
    salt = os.urandom(16)
    return str(hashlib.scrypt(password, salt=salt, n=2048, p=1, r=8))


@async_timed()
async def main():
    # loop = asyncio.get_running_loop()
    tasks = (asyncio.to_thread(hash_password, passwd) for passwd in passwords)

    # with ThreadPoolExecutor() as pool:
    #     for password in passwords:
    #         tasks.append(loop.run_in_executor(pool, hash_password, password))

    await asyncio.gather(*tasks)

# hash = hash_password

asyncio.run(main())
