from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from functools import partial
import aiohttp, asyncio


async def get_url_details(session: aiohttp.ClientSession, url: str):
    start_time = datetime.now()
    response = await session.get(url)
    response_body = await response.text()
    end_time = datetime.now()
    return {
        "status": response.status,
        "time": (end_time - start_time).microseconds,
        "body_length": len(response_body),
    }


async def make_requests(url: str, request_num: int):
    async with aiohttp.ClientSession() as session:
        requests = (get_url_details(session, url) for _ in range(request_num))
        results = await asyncio.gather(*requests, return_exceptions=True)
        failed_results = [str(r) for r in results if isinstance(r, Exception)]
        successful_results = [r for r in results if not isinstance(r, Exception)]
        return {
            "failed_results": failed_results,
            "successful_results": successful_results,
        }


async def requests_view(request):
    loop = asyncio.get_running_loop()
    print(f"EventLoopID: {hex(id(loop))}")
    url: str = request.GET["url"]
    request_num: int = int(request.GET["request_num"])
    context = await make_requests(url, request_num)
    return render(request, "async_api/requests.html", context)


def sleep(seconds: int):
    import time

    time.sleep(seconds)


async def sync_to_async_view(request):
    sleep_time: int = int(request.GET["sleep_time"])
    num_calls: int = int(request.GET["num_calls"])
    thread_sensitive: bool = request.GET["thread_sensitive"].lower() == "true"
    function = sync_to_async(
        partial(sleep, sleep_time), thread_sensitive=thread_sensitive
    )
    await asyncio.gather(*[function() for _ in range(num_calls)])
    return HttpResponse("")


def requests_view_sync(request):
    url: str = request.GET["url"]
    request_num: int = int(request.GET["request_num"])
    context = async_to_sync(partial(make_requests, url, request_num))()
    return render(request, "async_api/requests.html", context)
