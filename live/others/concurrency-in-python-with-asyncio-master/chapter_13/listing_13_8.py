import asyncio
import os
import random
import string
import time

GPG_PROGRAM = [
    "gpg",
    "-c",
    "--batch",
    "--passphrase",
    "3ncryptm3",
    "--cipher-algo",
    "TWOFISH",
]


async def encrypt(sem: asyncio.Semaphore, text: str) -> bytes:
    async with sem:
        process: asyncio.subprocess.Process = await asyncio.create_subprocess_exec(
            *GPG_PROGRAM, stdout=asyncio.subprocess.PIPE, stdin=asyncio.subprocess.PIPE
        )
        stdout, _ = await process.communicate(text.encode())
        return stdout


async def main():
    text_list = [
        "".join(random.choices(string.ascii_letters, k=1000)) for _ in range(1000)
    ]
    semaphore = asyncio.Semaphore(os.cpu_count() or 4)
    s = time.time()
    tasks = [asyncio.create_task(encrypt(semaphore, text)) for text in text_list]
    encrypted_text = await asyncio.gather(*tasks)
    e = time.time()

    print(f"Total time: {e - s}")


if __name__ == "__main__":
    asyncio.run(main())
