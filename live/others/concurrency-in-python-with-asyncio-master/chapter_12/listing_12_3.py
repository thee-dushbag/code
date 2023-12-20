import asyncio as aio
from random import randrange
from aiohttp import web


QUEUE_KEY = "order_queue"


async def process_order(worker_id: int, queue: aio.Queue):  # A
    print(f"Worker {worker_id}: Up and running.")
    try:
        while order := await queue.get():
            print(f"Worker {worker_id}: Processing order {order}")
            await aio.sleep(order)
            queue.task_done()
    except aio.CancelledError:
        print(f"Worker {worker_id}: Killed")
    finally:
        print(f"Worker {worker_id}: Shutting down.")


async def place_order(req: web.Request) -> web.Response:
    order_queue = req.app[QUEUE_KEY]
    await order_queue.put(randrange(1, 5))  # B
    return web.Response(body="Order placed!")


async def queue_ctx(app: web.Application):
    print("Creating order queue and processors.")
    queue = aio.Queue(10)
    workers = [aio.create_task(process_order(wid, queue)) for wid in range(5)]
    app[QUEUE_KEY] = queue
    app["wtasks"] = workers
    yield
    [w.cancel() for w in workers]
    await aio.gather(*workers)


async def _start(app: web.Application):
    print("Creating order queue and processors.")
    queue = aio.Queue(10)
    workers = [aio.create_task(process_order(wid, queue)) for wid in range(5)]
    app[QUEUE_KEY] = queue
    app["wtasks"] = workers


async def _stop(app: web.Application):
    workers = app["wtasks"]
    [w.cancel() for w in workers]
    await aio.gather(*workers)


routes = [web.get("/order", place_order)]


async def application():
    app = web.Application()
    app.on_startup.append(_start)
    app.on_cleanup.append(_stop)
    # app.cleanup_ctx.append(queue_ctx)
    app.add_routes(routes)
    return app


if __name__ == "__main__":
    web.run_app(application())
