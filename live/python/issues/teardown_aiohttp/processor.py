from aiohttp import web
import asyncio

QUEUE = "task_queue.app"
TASKS = "tasks_list.app"


# Infinite Task Generator
def tasks_generator(start: int = 1):
    while True:
        yield f"Task_{start}"
        start += 1


# Dummy infinite task generator.
GENERATOR = tasks_generator()


# For processing the incomming tasks in the Queue
async def processor(processor_id: int, tasks_queue: asyncio.Queue):
    print(f"Worker {processor_id}: Up and Running.")
    try:
        while True:
            task = await tasks_queue.get()
            print(f"Worker {processor_id}: Processing {task}.")
            await asyncio.sleep(2)  # Simulate some heavy processing.
            print(f'  Processed {task}.')
    except asyncio.CancelledError:
        print(f"Worker {processor_id}: Killed.")
    finally:
        print(f"Worker {processor_id}: Shutting down.")


# The processors lifetime is setup and destroyed here.
async def processor_ctx(app: web.Application):
    print("[plugin]: Starting processors.")
    queue = asyncio.Queue(5) # Only store 5 tasks at a time
    workers = [asyncio.create_task(processor(pid, queue)) for pid in range(1, 4)]
    app[QUEUE] = queue
    yield
    print("[plugin]: Stoping processors.")
    [w.cancel() for w in workers]
    await asyncio.gather(*workers)


# Create the processors and save in the background
async def processor_setup(app: web.Application):
    print("[plugin]: Starting processors.")
    queue = asyncio.Queue(5)
    workers = [asyncio.create_task(processor(pid, queue)) for pid in range(1, 4)]
    app[QUEUE] = queue
    app[TASKS] = workers


# Destroy the saved processors from above
async def processor_teardown(app: web.Application):
    print("[plugin]: Stoping processors.")
    workers = app[TASKS]
    [w.cancel() for w in workers]
    await asyncio.gather(*workers)


# Connect the plugin to our application.
def setup(app: web.Application, toggle: str = ""):
    """Control which setup-teardown to use using the toggle parameter"""
    if toggle == "ctx":
        app.cleanup_ctx.append(processor_ctx)
    else:
        app.on_startup.append(processor_setup)
        app.on_cleanup.append(processor_teardown)
