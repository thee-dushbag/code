import functools
from collections import defaultdict
from typing import Dict


def map_frequency(text: str) -> Dict[str, int]:
    words = text.split(" ")
    frequencies: dict[str, int] = defaultdict(lambda: 0)
    for word in words:
        frequencies[word] += 1
    return dict(frequencies)


def merge_dictionaries(first: Dict[str, int], second: Dict[str, int]) -> Dict[str, int]:
    merged = defaultdict(lambda: 0, first)
    for key in second:
        merged[key] += second[key]
    return dict(merged)


lines = [
    "I know what I know",
    "I know that I know",
    "I don't know much",
    "They don't know much",
]

mapped_results = [map_frequency(line) for line in lines]

for result in mapped_results:
    print(result)

print(functools.reduce(merge_dictionaries, mapped_results))
