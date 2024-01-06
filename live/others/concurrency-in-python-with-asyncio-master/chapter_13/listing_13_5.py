import asyncio


async def main():
    program = ["python3", "listing_13_4.py"]
    process = await asyncio.create_subprocess_exec(
        *program, stdout=asyncio.subprocess.PIPE
    )
    print(f"Process pid is: {process.pid}")
    return_code = await process.wait()
    print(f"Process returned: {return_code}")


if __name__ == "__main__":
    asyncio.run(main())
