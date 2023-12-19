import asyncio as aio


async def operation(semaphore: aio.Semaphore, task_id: int):
    print(f"Task: {task_id} pending")
    async with semaphore:
        print(f"Task: {task_id} running")
        await aio.sleep(task_id % 2 + 1)
    print(f"Task: {task_id} done")


async def main():
    semaphore = aio.Semaphore(2)
    tasks = (operation(semaphore, task_id) for task_id in range(1, 11))
    await aio.gather(*tasks)


if __name__ == "__main__":
    aio.run(main())
