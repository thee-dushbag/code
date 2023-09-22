import asyncio

import asyncpg
from asyncpg.transaction import Transaction

from __init__ import cred


async def main():
    connection = await asyncpg.connect(**cred)
    transaction: Transaction = connection.transaction()  # A
    await transaction.start()  # B
    try:
        await connection.execute("INSERT INTO brand " "VALUES(DEFAULT, 'brand_1')")
        await connection.execute("INSERT INTO brand " "VALUES(DEFAULT, 'brand_2')")
    except asyncpg.PostgresError:
        print("Errors, rolling back transaction!")
        await transaction.rollback()  # C
    else:
        print("No errors, committing transaction!")
        await transaction.commit()  # D

    query = """SELECT brand_name FROM brand 
                WHERE brand_name LIKE 'brand%'"""
    brands = await connection.fetch(query)
    print(brands)

    await connection.close()


asyncio.run(main())
