import asyncio

import asyncpg

from __init__ import cred


async def take(generator, to_take: int):
    item_count = 0
    async for item in generator:
        if item_count > to_take - 1:
            return
        item_count = item_count + 1
        yield item


async def main():
    connection = await asyncpg.connect(**cred)
    async with connection.transaction():
        query = "SELECT product_id, product_name from product"
        product_generator = connection.cursor(query)

        async for product in take(product_generator, 5):
            print(product)

        print("Got the first five products!")

    await connection.close()


asyncio.run(main())
