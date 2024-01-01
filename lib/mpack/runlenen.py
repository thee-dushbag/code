def encode(data: str) -> str:
    size, index, buffer = len(data), 0, []
    while index < size:
        char, count = data[index], 0
        while index < size:
            if data[index] != char:
                break
            count, index = count + 1, index + 1
        char = chr(ord(char) + 1)
        buffer.append(f"{char}{count}")
    return "\0".join(buffer)


def decode(data: str) -> str:
    buffer = ""
    for section in data.split("\0"):
        char, digit = section[0], int(section[1:] or "1")
        buffer += chr(ord(char) - 1) * digit
    return buffer


