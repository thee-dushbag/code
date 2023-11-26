import asyncio
from asyncio import AbstractEventLoop
from concurrent.futures import Future
from typing import Callable, Optional, Coroutine
from aiohttp import ClientSession

class StressTest:
    def __init__(
        self,
        loop: AbstractEventLoop,
        url: str,
        total_requests: int,
        callback: Callable[[int, int], Coroutine[None, None, None]],
    ):
        self._completed_requests: int = 1
        self._load_test_future: Optional[Future] = None
        self._loop = loop
        self._url = url
        self._total_requests = total_requests
        self._callback = callback
        self._refresh_rate = (total_requests // 100) or 2

    def start(self):
        future = asyncio.run_coroutine_threadsafe(self._make_requests(), self._loop)
        self._load_test_future = future

    def cancel(self):
        def cancel_none():
            if self._load_test_future:
                self._load_test_future.cancel()
                # print("Killed Stress Test")
            self._load_test_future = None

        self._loop.call_soon_threadsafe(cancel_none)  # B

    async def _get_url(self, session: ClientSession, url: str):
        # print(f"Getting URL: {self._url}")
        try:
            async with await session.get(url) as resp:
                resp.status
                # print(await resp.text())
        except Exception as e:
            print(f'Error: {e!r}')
        self._completed_requests += 1  # C
        if (
            not (self._completed_requests % self._refresh_rate)
            or self._completed_requests >= self._total_requests
        ):
            await self._callback(self._completed_requests, self._total_requests)

    async def _make_requests(self):
        # connector = TCPConnector(force_close=True, limit_per_host=50)
        async with ClientSession() as session:
            reqs = (
                self._get_url(session, self._url) for _ in range(self._total_requests)
            )
            await asyncio.gather(*reqs)
