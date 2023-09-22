import asyncio
import logging
import asyncpg
from __init__ import cred


async def main():
    connection = await asyncpg.connect(**cred)
    try:
        async with connection.transaction():
            insert_brand = "INSERT INTO brand VALUES(9999, 'big_brand')"
            await connection.execute(insert_brand)
            await connection.execute(insert_brand)  # A
    except Exception:
        logging.exception('Error while running transaction')  # B
    finally:
        query = """SELECT brand_name FROM brand 
                    WHERE brand_name LIKE 'big_%'"""
        brands = await connection.fetch(query)  # C
        print(f'Query result was: {brands}')

        await connection.close()


asyncio.run(main())
