import asyncio
from asyncio import AbstractEventLoop
from threading import Thread

from listing_7_14 import LoadTester


class ThreadedEventLoop(Thread):  # A
    def __init__(self, loop: AbstractEventLoop):
        super().__init__()
        self._loop = loop
        self.daemon = True

    def run(self):
        try:
            self._loop.run_forever()
        finally:
            self._loop.stop()


loop = asyncio.new_event_loop()

asyncio_thread = ThreadedEventLoop(loop)
asyncio_thread.start()  # B

app = LoadTester(loop)  # C
app.mainloop()
