import sys
from asyncio import StreamReader
from collections import deque

from listing_8_7 import clear_line, move_back_one_char


async def read_line(stdin_reader: StreamReader) -> str:
    def erase_last_char():
        move_back_one_char()
        sys.stdout.write(" ")
        move_back_one_char()

    delete_char = b"\x7f"
    input_buffer = deque()
    while (input_char := await stdin_reader.read(1)) != b"\n":
        if input_char == delete_char and input_buffer:
            input_buffer.pop()
            erase_last_char()
            sys.stdout.flush()
            continue
        input_buffer.append(input_char)
        sys.stdout.write(input_char.decode())
        sys.stdout.flush()
    clear_line()
    return b"".join(input_buffer).decode()
