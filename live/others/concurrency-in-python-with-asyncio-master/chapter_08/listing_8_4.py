import asyncio

from util import delay


# Creating a new thread just to get
# user input is resource wasteful.
async def ainput(prompt: str = '') -> str:
    '''Gets the job done, but very expensive.
    Definately non-blocking.'''
    return await asyncio.to_thread(input, prompt)

async def main():
    while True:
        delay_time = input("Enter a time to sleep:") # Blocking
        # delay_time = await ainput("Enter a time to sleep:") # Non-blocking
        asyncio.create_task(delay(int(delay_time)))
        # await asyncio.sleep(0)

asyncio.run(main())
