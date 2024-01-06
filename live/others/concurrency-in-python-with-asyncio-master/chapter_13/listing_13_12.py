import asyncio


async def consume_and_send(
    text_list, stdout: asyncio.StreamReader, stdin: asyncio.StreamWriter
):
    for text in text_list:
        line = await stdout.read(50)
        print(line.decode())
        stdin.write(text.encode())
        await stdin.drain()


async def main():
    program = "python3", "listing_13_11.py"
    process = await asyncio.create_subprocess_exec(
        *program, stdout=asyncio.subprocess.PIPE, stdin=asyncio.subprocess.PIPE
    )
    assert process.stdin and process.stdout
    text_input = "Simon\n", "Nganga\n", "Njeri\n", "Faith\n", "\n"
    consume_feed = consume_and_send(text_input, process.stdout, process.stdin)
    await asyncio.gather(consume_feed, process.wait())


if __name__ == "__main__":
    asyncio.run(main())
