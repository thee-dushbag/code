from string import ascii_letters
from random import choices, choice

const_sizes = list(range(1, 50))


def getletters(allletters=None):
    letters = set(allletters or ascii_letters)

    def getletter():
        assert letters
        letter = choice(list(letters))
        letters.remove(letter)
        return letter

    return getletter


def runlengthdecoder(string: str) -> str:
    digit, buffer = "", ""
    for char in string:
        if char.isdigit():
            digit += char
            continue
        buffer += char * int(digit or "1")
        digit = ""
    return buffer


def runlengthencoder(string: str):
    """Lossless string compression, only [a-zA-Z]* strings.
    Uses Run-Length-Compression Algorithm"""
    size, index, buffer = len(string), 0, ""
    while index < size:
        current_char, count = string[index], 0
        while index < size:
            if string[index] != current_char:
                break
            count, index = count + 1, index + 1
        buffer += f"{count if count > 1 else ''}{current_char}"
    return buffer


def _runlengthtest(tester):
    for _ in range(100):
        for size in range(52):
            sizes = choices(const_sizes, k=size)
            getletter = getletters(ascii_letters)
            letters = (getletter() for _ in range(size))
            encoded, decoded = "", ""
            for size, letter in zip(sizes, letters):
                decoded += letter * size
                encoded += f"{size if size > 1 else ''}{letter}"
            tester(decoded, encoded)


def test_runlengthdecoder():
    def tester(decoded, encoded):
        assert runlengthdecoder(encoded) == decoded

    _runlengthtest(tester)


def test_runlengthencoder():
    def tester(decoded, encoded):
        assert encoded == runlengthencoder(decoded)

    _runlengthtest(tester)
