import dataclasses as dt
import asyncio


@dt.dataclass(order=True)
class WorkItem:
    priority: int
    data: str = dt.field(compare=False)


async def worker(queue: asyncio.Queue):
    while not queue.empty():
        work_item: WorkItem = await queue.get()
        print(f"Processing work item {work_item}")
        queue.task_done()


async def main():
    priority_queue = asyncio.PriorityQueue()
    work_items = [
        WorkItem(3, "Lowest priority"),
        WorkItem(3, "Lowest priority second"),
        WorkItem(3, "Lowest priority third"),
        WorkItem(2, "Medium priority"),
        WorkItem(1, "High priority"),
    ]

    worker_task = asyncio.create_task(worker(priority_queue))

    for work in work_items:
        priority_queue.put_nowait(work)

    await asyncio.gather(priority_queue.join(), worker_task)


if __name__ == "__main__":
    asyncio.run(main())
