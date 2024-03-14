import asyncio
import typing
import click
import os


async def processor(data: asyncio.Queue[str], delay: float):
    while True:
        item = await data.get()
        data.task_done()
        if item is None:
            return
        print(f"Processed: {item!r}")
        await asyncio.sleep(delay)


class ProcessorServer:
    def __init__(self, delay: float, max_tasks: int) -> None:
        self._data: asyncio.Queue[str] = asyncio.Queue(maxsize=max_tasks)
        self._processor = asyncio.create_task(processor(self._data, delay))

    async def serve(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        try:
            while True:
                if not (buffer := await reader.readline()):
                    break
                writer.write(b"Received task successfully.\n")
                await writer.drain()
                await self._data.put(buffer.decode()[:-1])
        except (asyncio.CancelledError, ConnectionResetError, BrokenPipeError):
            ...

    async def wait_closed(self):
        await self._data.put(None)  # type: ignore
        await self._data.join()
        await self._processor


default_path = "./socket.sock"


async def client(stop: int, path: str):
    from mpack.number_reader import get_reader

    read_eng = get_reader("english")
    messages = range(1, stop + 1)
    try:
        reader, writer = await asyncio.open_unix_connection(path)
        current: str
        for current in map(read_eng, messages):
            print(f"Sending: {current!r}")
            writer.write(current.encode() + b"\n")
            await writer.drain()
            ack = await reader.readline()
            print(ack.decode()[:-1])
        writer.close()
        await writer.wait_closed()
    except FileNotFoundError:
        print(f"Make sure the server is running as {path} was not found.")
    except ConnectionResetError:
        print("Server disconnected.")
    except BrokenPipeError:
        print("Connection endpoint might have been destroyed.")


async def server(delay: float, path: str, max_tasks: int):
    processor_server = ProcessorServer(delay, max_tasks)
    server = await asyncio.start_unix_server(processor_server.serve, path)
    try:
        async with server:
            await server.serve_forever()
    except asyncio.CancelledError:
        ...
    if os.path.exists(path):
        os.remove(path)
    await processor_server.wait_closed()


T = typing.TypeVar("T")

Runner = typing.Callable[[typing.Coroutine[T, None, None]], T]


def wrap_runner(run):
    def pass_args(debug: bool):
        def runner(main: typing.Coroutine[T, None, None], /) -> T:
            return run(main, debug=debug)

        return runner

    return pass_args


def get_uvloop_runner():
    try:
        import uvloop
    except ImportError:
        raise click.BadParameter("UvLoop Not installed")
    return wrap_runner(uvloop.run)


def get_asyncio_runner():
    return wrap_runner(asyncio.run)


runners = dict(asyncio=get_asyncio_runner, uvloop=get_uvloop_runner)


@click.group
@click.option("--runner", "-r", type=click.Choice(["asyncio", "uvloop"]))
@click.option("--asyncio", "runner", flag_value="asyncio", default=True)
@click.option("--uvloop", "runner", flag_value="uvloop")
@click.option("--debug", "-d", is_flag=True, default=False)
@click.pass_context
def app(ctx: click.Context, runner: str, debug: bool):
    get_runner = runners[runner]()
    ctx.obj = get_runner(debug=debug)


@app.command("server")
@click.option("--delay", "-d", type=click.FloatRange(min=0, max=1), default=0.5)
@click.option("--path", "-p", type=click.Path(exists=False), default=default_path)
@click.option("--max", "maxsize", type=click.IntRange(min=1, max=float("inf")))
@click.pass_obj
def server_command(run: Runner[None], delay: float, path: str, maxsize: int | None):
    maxsize = -1 if maxsize is None else maxsize
    run(server(delay, path, maxsize))


@app.command("client")
@click.option("--stop", "-s", type=click.IntRange(1, 100), prompt=True)
@click.option("--path", "-p", type=click.Path(exists=False), default=default_path)
@click.pass_obj
def client_command(run: Runner[None], stop: int, path: str):
    run(client(stop, path))


if __name__ == "__main__":
    app()
