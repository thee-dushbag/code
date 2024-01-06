import asyncio
from asyncio import StreamReader


async def write_output(prefix: str, stdout: StreamReader):
    while line := await stdout.readline():
        print(f"[{prefix}]: {line.rstrip().decode()}")


async def main():
    program: tuple[str, str] = "ls", "-la"
    process = await asyncio.create_subprocess_exec(
        *program, stdout=asyncio.subprocess.PIPE
    )
    assert process.stdout is not None
    print(f"Process pid is: {process.pid}")
    stdout_task = asyncio.create_task(write_output(" ".join(program), process.stdout))

    *return_code, _, _ = await asyncio.gather(process.wait(), stdout_task)
    print(f"Processes returned: {str(return_code)[1:-1]}")


if __name__ == "__main__":
    asyncio.run(main())
