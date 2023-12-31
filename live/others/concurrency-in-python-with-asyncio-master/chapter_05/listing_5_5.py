import asyncio
from random import sample
from typing import Any, List, Tuple, Union
from pathlib import Path

import asyncpg

common_words_path = Path(__file__).parent / 'common_words.txt'

from __init__ import cred


def load_common_words() -> List[str]:
    with common_words_path.open() as common_words:
        return common_words.readlines()


def generate_brand_names(words: List[str]) -> List[Tuple[Union[str, Any]]]:
    return [(words[index],) for index in sample(range(100), 100)]


async def insert_brands(common_words, connection) -> int:
    brands = generate_brand_names(common_words)
    insert_brands = "INSERT INTO brand VALUES(DEFAULT, $1)"
    return await connection.executemany(insert_brands, brands)


async def main():
    common_words = load_common_words()
    connection: asyncpg.Connection = await asyncpg.connect(**cred)
    await insert_brands(common_words, connection)
    await connection.close()

if __name__ == '__main__':
    asyncio.run(main())
