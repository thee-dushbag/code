import asyncio
from asyncio.subprocess import Process


async def main():
    process: Process = await asyncio.create_subprocess_exec("sleep", "10")
    print(f"Process pid is: {process.pid}")
    status_code = await process.wait()  # Block until the process teminates
    print(f"Status code: {status_code}")


if __name__ == "__main__":
    asyncio.run(main())
