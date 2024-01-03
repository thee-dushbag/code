import asyncio
import logging
from asyncio import Queue

import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup


class CrawlTracker:
    def __init__(self, max_depth: int) -> None:
        self.queue = Queue()
        self.visited: dict[str, str] = {}
        self.max_depth = max_depth


class WorkItem:
    def __init__(self, item_depth: int, url: str):
        self.item_depth = item_depth
        self.url = url


async def worker(
    worker_id: int,
    queue: Queue[WorkItem],
    session: ClientSession,
    tracker: CrawlTracker,
):
    print(f"Worker {worker_id}")
    while True:  # A
        work_item: WorkItem = await queue.get()
        print(f"Worker {worker_id}: Processing {work_item.url}")
        await process_page(work_item, queue, session, tracker)
        print(f"Worker {worker_id}: Finished {work_item.url}")
        queue.task_done()


async def process_page(
    work_item: WorkItem, queue: Queue, session: ClientSession, tracker: CrawlTracker
):  # B
    try:
        if work_item.item_depth == tracker.max_depth:
            print(f"Max depth reached, not processing more for {work_item.url}")
            return
        response = await asyncio.wait_for(session.get(work_item.url), timeout=3)
        if str(response.url) in tracker.visited:
            return
        body = await response.text()
        soup = BeautifulSoup(body, "html.parser")
        head = soup.find("h1")
        tracker.visited[str(response.url)] = "" if head is None else head.text
        links = soup.find_all("a", href=True)
        for link in links:
            queue.put_nowait(WorkItem(work_item.item_depth + 1, link["href"]))
    except Exception:
        logging.exception(f"Error processing url {work_item.url}")


async def main():  # C
    start_url = "http://0.0.0.0:8080"
    url_queue = Queue()
    url_queue.put_nowait(WorkItem(0, '/six.html'))
    tracker = CrawlTracker(3)
    async with aiohttp.ClientSession(base_url=start_url) as session:
        workers = [
            asyncio.create_task(worker(i, url_queue, session, tracker))
            for i in range(3)
        ]
        await url_queue.join()
        [w.cancel() for w in workers]
    print(tracker.visited)


if __name__ == "__main__":
    asyncio.run(main())
