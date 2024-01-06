import asyncio


async def main():
    program = ["python3", "listing_13_4.py"]
    process = await asyncio.create_subprocess_exec(
        *program, stdout=asyncio.subprocess.PIPE
    )
    print(f"Process pid is: {process.pid}")
    stdout, stderr = await process.communicate()
    print(stdout, stderr)
    print(f"Process returned: {process.returncode}")


if __name__ == "__main__":
    asyncio.run(main())
