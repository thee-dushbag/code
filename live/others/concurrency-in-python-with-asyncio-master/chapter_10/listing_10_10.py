import asyncio, listing_10_9 as ret

async def main():
    async def always_fail():
        raise Exception("I've failed!")

    async def always_timeout():
        await asyncio.sleep(1)

    async def always_return():
        return 34

    try:
        await ret.retry(always_fail, max_retries=3, timeout=0.1, retry_interval=0.1)
    except ret.TooManyRetries:
        print("Retried too many times!")

    try:
        await ret.retry(always_timeout, max_retries=3, timeout=0.1, retry_interval=0.1)
    except ret.TooManyRetries:
        print("Retried too many times!")

    v = await ret.retry(always_return, max_retries=3, timeout=1, retry_interval=1)
    print(f"Received value: {v}")


if __name__ == "__main__":
    asyncio.run(main())
