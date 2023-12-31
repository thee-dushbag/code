import asyncio

import asyncpg

from __init__ import cred


async def main():
    connection = await asyncpg.connect(**cred)
    async with connection.transaction():
        query = "SELECT product_id, product_name from product"
        cursor = await connection.cursor(query)  # A
        await cursor.forward(500)  # B
        products = await cursor.fetch(100)  # C
        for product in products:
            print(product)

    await connection.close()


if __name__ == '__main__':
    asyncio.run(main())
