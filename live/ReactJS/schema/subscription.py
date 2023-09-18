from string import Template
import strawberry as straw, asyncio as aio, typing as ty
import schema._defs as defs
import schema._schema as scheme
from strawberry.types import Info
from itertools import count
from strawberry.subscriptions.protocols.graphql_transport_ws.types import PingMessage


@straw.type
class Subscription:
    @straw.subscription
    async def echo(
        self, message: str, delay: float = 0
    ) -> ty.AsyncGenerator[str, None]:
        await aio.sleep(delay)
        yield message

    @straw.subscription
    async def request_ping(
        self, info: Info[ty.Any, ty.Any]
    ) -> ty.AsyncGenerator[bool, None]:
        ws = info.context["ws"]
        await ws.send_json(PingMessage().as_dict())
        yield True

    @straw.subscription
    async def infinity(
        self, message: str, delay: ty.Optional[float] = None
    ) -> ty.AsyncGenerator[str, None]:
        for cnt in count(1):
            yield f"[{cnt}] Message: {message!r}"
            await aio.sleep(delay or 1)

    @straw.subscription
    async def counter(self, message: str, delay: ty.Optional[float] = None) -> ty.AsyncGenerator[str, None]:
        template = Template(message)
        delay = delay or 0.5
        for i in count(1):
            yield template.substitute(count=i)
            await aio.sleep(delay)

    @straw.subscription
    async def context(self, info: Info[ty.Any, ty.Any]) -> ty.AsyncGenerator[str, None]:
        yield info.context["custom_value"]

    @straw.subscription
    async def error(self, message: str) -> ty.AsyncGenerator[str, None]:
        yield GraphQLError(message)  # type: ignore

    @straw.subscription
    async def exception(self, message: str) -> ty.AsyncGenerator[str, None]:
        raise ValueError(message)

        # Without this yield, the method is not recognised as an async generator
        yield "Hi"

    @straw.subscription
    async def flavors(self) -> ty.AsyncGenerator[defs.Flavor, None]:
        for flavor in list(defs.Flavor):
            yield flavor
            await aio.sleep(1)

    @straw.subscription
    async def flavors_invalid(self) -> ty.AsyncGenerator[defs.Flavor, None]:
        yield defs.Flavor.VANILLA
        yield "Invalid defs.Flavor Over HERE!!!"  # type: ignore
        yield defs.Flavor.CHOCOLATE

    @straw.subscription
    async def debug(
        self, info: Info[ty.Any, ty.Any]
    ) -> ty.AsyncGenerator[scheme.DebugInfo, None]:
        active_result_handlers = [
            task for task in info.context["get_tasks"]() if not task.done()
        ]

        connection_init_timeout_task = info.context["connectionInitTimeoutTask"]
        is_connection_init_timeout_task_done = (
            connection_init_timeout_task.done()
            if connection_init_timeout_task
            else None
        )

        yield scheme.DebugInfo(
            num_active_result_handlers=len(active_result_handlers),
            is_connection_init_timeout_task_done=is_connection_init_timeout_task_done,
        )

    @straw.subscription
    async def listener(
        self,
        info: Info[ty.Any, ty.Any],
        timeout: ty.Optional[float] = None,
        group: ty.Optional[str] = None,
    ) -> ty.AsyncGenerator[str, None]:
        yield info.context["request"].channel_name

        async for message in info.context["request"].channel_listen(
            type="test.message",
            timeout=timeout,
            groups=[group] if group is not None else [],
        ):
            yield message["text"]

    @straw.subscription
    async def listener_with_confirmation(
        self,
        info: Info[ty.Any, ty.Any],
        timeout: ty.Optional[float] = None,
        group: ty.Optional[str] = None,
    ) -> ty.AsyncGenerator[ty.Union[str, None], None]:
        async with info.context["request"].listen_to_channel(
            type="test.message",
            timeout=timeout,
            groups=[group] if group is not None else [],
        ) as cm:
            yield None
            yield info.context["request"].channel_name
            async for message in cm:
                yield message["text"]

    @straw.subscription
    async def connection_params(
        self, info: Info[ty.Any, ty.Any]
    ) -> ty.AsyncGenerator[str, None]:
        yield info.context["connection_params"]["straw"]

    @straw.subscription
    async def long_finalizer(
        self, info: Info[ty.Any, ty.Any], delay: float = 0
    ) -> ty.AsyncGenerator[str, None]:
        try:
            for _i in range(100):
                yield "hello"
                await aio.sleep(0.01)
        finally:
            await aio.sleep(delay)
