import asyncio

import asyncpg

from __init__ import cred


async def main():
    connection = await asyncpg.connect(**cred)

    query = "SELECT product_id, product_name FROM product"
    async with connection.transaction():
        async for product in connection.cursor(query):
            print(f"id: {product['product_id']} | name: {product['product_name']!r}")

    await connection.close()


asyncio.run(main())
