import asyncio, logging, typing as ty


class TooManyRetries(Exception):
    pass

async def retry(
    coro: ty.Callable[[], ty.Awaitable],
    max_retries: int,
    timeout: float,
    retry_interval: float,
):
    for retry_num in range(max_retries):
        try:
            return await asyncio.wait_for(coro(), timeout=timeout)
        except Exception as e:
            logging.error(
                f"Exception while waiting (tried {retry_num + 1} times), retrying.",
                # exc_info=ec,
            )
            await asyncio.sleep(retry_interval)
    raise TooManyRetries()
