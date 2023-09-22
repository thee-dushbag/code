import asyncpg
import asyncio
from __init__ import cred


async def main():
    connection = await asyncpg.connect(**cred)
    version = connection.get_server_version()
    print(f'Connected! Postgres version is {version}')
    await connection.close()


asyncio.run(main())
