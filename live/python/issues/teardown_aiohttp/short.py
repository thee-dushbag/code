from itertools import count
from aiohttp import web
import asyncio

QUEUE, TASK = "QUEUE", "TASK"


# -------------------------------------------------------------------------------------


# Create the worker and save in the background
async def worker_setup(app: web.Application):
    print("[plugin]: Starting worker.")
    app[QUEUE] = asyncio.Queue(3)  # Only store 3 tasks at a time
    app[TASK] = asyncio.create_task(worker(app[QUEUE]))


# Destroy the saved worker from above
async def worker_teardown(app: web.Application):
    print("[plugin]: Stopping worker.")
    await app[QUEUE].join()
    app[TASK].cancel()
    await app[TASK]


async def worker_seted(app: web.Application):
    await worker_setup(app)
    yield
    await worker_teardown(app)


async def worker_ctx(app: web.Application):
    async with SimpleCTX(app, worker_setup, worker_teardown):
        yield


# Connect the plugin to our application.
def installer(app: web.Application):
    """Control which setup-teardown using the argv[1] passed in"""
    from sys import argv
    CTX_TYPE = argv[1] if len(argv) > 2 else ""

    if CTX_TYPE == "seted":
        app.cleanup_ctx.append(worker_seted)
    elif CTX_TYPE == "ctx":
        app.cleanup_ctx.append(worker_ctx)
    else:
        app.on_startup.append(worker_setup)
        app.on_cleanup.append(worker_teardown)


async def worker(tasks_queue: asyncio.Queue):
    print(f"Worker: Up and Running.")
    try:
        await workon(tasks_queue)
    except asyncio.CancelledError:
        print(f"Worker: Killed.")
    finally:
        print(f"Worker: Shutting down.")


# -------------------------------------------------------------------------------------


class SimpleCTX:
    def __init__(self, app, enter, exit) -> None:
        self.app = app
        self.enter = enter
        self.exit = exit

    async def __aenter__(self):
        await self.enter(self.app)

    async def __aexit__(self, *errs):
        await self.exit(self.app)


# Actual processing
async def workon(queue: asyncio.Queue):
    while True:
        task = await queue.get()
        print(f"Worker: Processing Task {task}.")
        await asyncio.sleep(0.5)  # Simulate some heavy processing.
        queue.task_done()


# Task Generator
GENERATOR = count(1)


async def enqueue_task(req: web.Request):
    queue = req.app[QUEUE]
    await queue.put(next(GENERATOR))  # Add task to be processed
    return web.Response()


app = web.Application()
installer(app)
app.router.add_get("/", enqueue_task)

try:
    web.run_app(app)
except KeyboardInterrupt:
    ...
