from fmt import Person
import asyncio as aio
import pickle
from pathlib import Path
from faker import Faker
import click

fake = Faker()


async def mainapp(count: int):
    path = Path.cwd() / "people.sock"
    for current in range(count):
        reader, writer = await aio.open_unix_connection(path)
        me = Person(fake.name(), fake.random.randint(18, 50))
        writer.write(pickle.dumps(me))
        writer.write_eof()
        await writer.drain()
        ack = await reader.read()
        print(current, ack.decode(), sep=": ")


@click.command()
@click.option("--count", "-c", type=int, default=3)
def main(count: int):
    aio.run(mainapp(count))


if __name__ == "__main__":
    main()
