from fmt import Person
import asyncio as aio
import pickle, contextlib
from pathlib import Path


@contextlib.contextmanager
def remove_path(path: str | Path):
    yield
    print("Removing: %s" % path)
    Path(path).unlink(True)

people: aio.Queue[Person]

async def introduce_people():
    while True:
        person = await people.get()
        people.task_done()
        if person is None:
            break
        print("Introducing %s" % person.name)
        print(person.introduce_self())
        await aio.sleep(2)

async def intro_person(reader: aio.StreamReader, writer: aio.StreamWriter):
    try:
        buffer = b""
        while chunk := await reader.read():
            buffer += chunk
        person: Person = pickle.loads(buffer)
        writer.write(b"Person received successfully.")
        await writer.drain()
        people.put_nowait(person)
    except Exception:
        ...
    writer.close()
    await writer.wait_closed()


async def main():
    path = Path.cwd() / "people.sock"
    global people
    task = aio.create_task(introduce_people())
    people = aio.Queue()
    server = await aio.start_unix_server(intro_person, path)
    with remove_path(path):
        try:
            async with server:
                await server.serve_forever()
        except aio.CancelledError as e:
            print("Stopped Serving: %s" % e.__class__.__name__)
    await people.join()
    people.put_nowait(None) # type: ignore
    await task

if __name__ == "__main__":
    aio.run(main())
