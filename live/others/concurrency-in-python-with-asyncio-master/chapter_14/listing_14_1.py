import asyncio, time


class TaskRunner:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.tasks = []

    def add_task(self, func):
        self.tasks.append(func)

    async def _run_all(self):
        atasks = []
        for task in self.tasks:
            task = task() if asyncio.iscoroutinefunction(task) else task
            atasks.append(
                asyncio.create_task(task)
                if asyncio.iscoroutine(task)
                else asyncio.to_thread(task)
            )
        await asyncio.gather(*atasks)

    def reset(self):
        self.tasks.clear()

    def run(self):
        self.loop.run_until_complete(self._run_all())


if __name__ == "__main__":

    def regular_function():
        print("Hello from a regular function!")
        time.sleep(3)
        print("Regular finished sleeping!")

    async def coroutine_function():
        print("Running coroutine, sleeping!")
        await asyncio.sleep(1)
        print("Finished sleeping!")

    runner = TaskRunner()
    runner.add_task(coroutine_function)
    runner.add_task(coroutine_function())
    runner.add_task(regular_function)
    runner.run()
