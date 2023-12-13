from listing_10_11 import CircuitBreaker
import asyncio


async def main():
    async def slow_callback():
        await asyncio.sleep(2)

    cb = CircuitBreaker(
        slow_callback, timeout=1.0, time_window=5, max_failures=2, reset_interval=5
    )

    for _ in range(4):
        try: await cb.request()
        except Exception: pass

    print("Sleeping for 5 seconds so breaker closes...")
    await asyncio.sleep(5)

    for _ in range(4):
        try: await cb.request()
        except Exception: pass

if __name__ == '__main__':
    asyncio.run(main())
