# from queue import Queue
from tkinter import Entry, Label, Tk, ttk
from typing import Optional
from janus import Queue
from asyncio import Lock as ALock
from threading import Lock

from listing_7_13 import StressTest

class LoadTester(Tk):
    def __init__(self, loop, *args, **kwargs):  # A
        Tk.__init__(self, *args, **kwargs)
        self._queue = Queue(loop=loop)
        self._refresh_ms = 25
        self._alock = ALock()
        self._lock = Lock()

        self._loop = loop
        self._load_test: Optional[StressTest] = None
        self.title("URL Requester")

        self._url_label = Label(self, text="URL:")
        self._url_label.grid(column=0, row=0)

        self._url_field = Entry(self, width=10)
        self._url_field.grid(column=1, row=0)

        self._request_label = Label(self, text="Number of requests:")
        self._request_label.grid(column=0, row=1)

        self._request_field = Entry(self, width=10)
        self._request_field.grid(column=1, row=1)

        self._submit = ttk.Button(self, text="Submit", command=self._start)  # B
        self._submit.grid(column=2, row=1)

        self._pb_label = Label(self, text="Progress:")
        self._pb_label.grid(column=0, row=3)

        self._pb = ttk.Progressbar(
            self, orient="horizontal", length=200, mode="determinate"
        )
        self._pb.grid(column=1, row=3, columnspan=2)

    def _update_bar(self, pct: int):  # C
        if pct >= 100:
            if self._load_test:
                self._load_test.cancel()
                self._load_test = None
            self._submit["text"] = "Submit"
            pct = 100
        else:
            self.after(self._refresh_ms, self._poll_queue)
        self._pb["value"] = pct

    def _queue_update(self, completed_requests: int, total_requests: int):  # D
        with self._lock:
            self._queue.sync_q.put(round((completed_requests / total_requests) * 100))

    async def _aqueue_update(self, completed_requests: int, total_requests: int):  # D
        async with self._alock:
            await self._queue.async_q.put(round((completed_requests / total_requests) * 100))

    def _poll_queue(self):  # E
        if not self._queue.sync_q.empty():
            percent_complete = self._queue.sync_q.get()
            self._update_bar(percent_complete)
        elif self._load_test:
            self.after(self._refresh_ms, self._poll_queue)

    def _start(self):  # F
        if self._load_test is None:
            self._submit["text"] = "Cancel"
            test = StressTest(
                self._loop,
                self._url_field.get(),
                int(self._request_field.get()),
                self._aqueue_update,
            )
            self.after(self._refresh_ms, self._poll_queue)
            test.start()
            self._load_test = test
        else:
            self._load_test.cancel()
            self._load_test = None
            self._submit["text"] = "Submit"
