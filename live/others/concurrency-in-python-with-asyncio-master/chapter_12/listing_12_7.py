import aiohttp.web as web
import dataclasses as dt
import asyncio
import random
import enum


QUEUE_KEY = "order_queue"


class UserType(enum.IntEnum):
    POWER_USER = 1
    NORMAL_USER = 2


@dt.dataclass(order=True)
class Order:
    user_type: UserType
    order_delay: int = dt.field(compare=False)


async def process_order_worker(worker_id: int, queue: asyncio.Queue):
    while True:
        print(f"Worker {worker_id}: Waiting for an order...")
        order = await queue.get()
        print(f"Worker {worker_id}: Processing order {order}")
        await asyncio.sleep(order.order_delay)
        print(f"Worker {worker_id}: Processed order {order}")
        queue.task_done()


async def place_order(request: web.Request) -> web.Response:
    body = await request.json()
    user_type = UserType.POWER_USER if body["power_user"] else UserType.NORMAL_USER
    order_queue = request.app[QUEUE_KEY]
    await order_queue.put(Order(user_type, random.randrange(5, 10)))
    return web.Response(body="Order placed!")


async def order_queue_ctx(app: web.Application):
    print("Creating order queue and tasks.")
    app[QUEUE_KEY] = q = asyncio.PriorityQueue(10)
    order_tasks = [asyncio.create_task(process_order_worker(i, q)) for i in range(1, 3)]
    yield
    try:
        print("Waiting for pending queue workers to finish....")
        await asyncio.wait_for(q.join(), timeout=10)
    finally:
        print("Finished all pending items, canceling worker tasks...")
        [task.cancel() for task in order_tasks]


async def app():
    app = web.Application()
    app.cleanup_ctx.append(order_queue_ctx)
    app.router.add_post("/order", place_order)
    return app


if __name__ == "__main__":
    web.run_app(app())
