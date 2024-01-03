import asyncio as aio
from random import randrange
from aiohttp import web


QUEUE_KEY = "order_queue"


async def process_order(worker_id: int, queue: aio.Queue):  # A
    print(f"Worker {worker_id}: Up and running.")
    free, order = True, None
    try:
        while order := await queue.get():
            free = False
            print(f"Worker {worker_id}: Processing order {order}")
            queue.task_done()
            free = True
            await aio.sleep(order)
    except aio.CancelledError:
        if not free:
            print(f"{worker_id}: Abandoned order: {order}")
            queue.task_done()
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
    yield
    for worker in workers:
        worker.cancel()
    await aio.gather(*workers)


routes = [web.get("/order", place_order)]


async def application():
    app = web.Application()
    app.cleanup_ctx.append(queue_ctx)
    app.add_routes(routes)
    return app


if __name__ == "__main__":
    web.run_app(application())
