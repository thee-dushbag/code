import asyncio, threading, concurrent.futures


async def greet(name: str, *, delay: float = 0.5):
    print(f"Hello {name}, how was your day?")
    await asyncio.sleep(delay)
    print(f"Goodbye {name}!")


class Greeter(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        self._M_loop = asyncio.new_event_loop()

    def run(self):
        self._M_loop.run_forever()

    def __enter__(self):
        self.start()
        return self

    def join(self):
        if self._M_loop.is_running():
            stop_event = threading.Event()
            self._M_loop.call_soon_threadsafe(stop_event.set)
            self._M_loop.stop()
            stop_event.wait()
        super().join()

    def __exit__(self, *_):
        self.join()

    def greet(self, name: str, *, delay: float = 0.5) -> concurrent.futures.Future[None]:
        return asyncio.run_coroutine_threadsafe(greet(name, delay=delay), self._M_loop)


def main():
    with Greeter() as greeter:
        names = ["Simon", "Faith", "Nganga", "Njeri", "Lydia", "Wanjiru"]
        greets = [greeter.greet(name, delay=1) for name in names]
        concurrent.futures.wait(greets)


if __name__ == "__main__":
    main()
