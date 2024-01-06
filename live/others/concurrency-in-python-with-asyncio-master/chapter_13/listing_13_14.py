import asyncio


async def output_consumer(
    input_ready_event: asyncio.Event, stdout: asyncio.StreamReader
):
    while data := await stdout.read(2048):
        print(data.decode())
        if data.endswith(b"Name: "):
            input_ready_event.set()


async def input_writer(
    text_data, input_ready_event: asyncio.Event, stdin: asyncio.StreamWriter
):
    for text in text_data:
        await input_ready_event.wait()
        stdin.write(text.encode())
        await stdin.drain()
        input_ready_event.clear()


async def main():
    program = "python3", "listing_13_13.py"
    process = await asyncio.create_subprocess_exec(
        *program, stdout=asyncio.subprocess.PIPE, stdin=asyncio.subprocess.PIPE
    )

    input_ready_event = asyncio.Event()
    assert process.stdin and process.stdout
    text_input = "Simon\n", "Nganga\n", "Faith\n", "Njeri\n", "\n"

    await asyncio.gather(
        output_consumer(input_ready_event, process.stdout),
        input_writer(text_input, input_ready_event, process.stdin),
        process.wait(),
    )


if __name__ == "__main__":
    asyncio.run(main())
