import strawberry as straw, typing as ty, asyncio as aio
import schema._schema as scheme
from strawberry.types import Info
from aiohttp import web
import schema._defs as defs


@straw.type
class Query:
    @straw.field
    async def company(self) -> defs.Company:
        return await defs.Company.create()

    @straw.field
    async def person(self) -> defs.Person:
        return await defs.Person.create()

    @straw.field
    async def named(self, type: defs.NamedEnum = defs.NamedEnum.PERSON) -> defs.Named:
        match type:
            case defs.NamedEnum.PERSON:
                return await defs.Person.create()  # type: ignore
            case defs.NamedEnum.COMPANY:
                return await defs.Company.create()  # type: ignore

    @straw.field
    def greetings(self) -> str:
        return "hello"

    @straw.field
    async def names(self, size: int) -> ty.List[str]:
        if size > 100:
            raise web.HTTPBadRequest(reason="Size too large: size < 100")
        return [defs.fake.name() for _ in range(size)]

    @straw.field
    async def describe(self, name: str, flavor: defs.Flavor) -> str:
        return f"Hello {name}, you like {flavor}."

    @straw.field
    def hello(self, name: ty.Optional[str] = None) -> str:
        return f"Hello {name or 'world'}"

    @straw.field
    async def async_hello(self, name: ty.Optional[str] = None, delay: float = 0) -> str:
        await aio.sleep(delay)
        return f"Hello {name or 'world'}"

    @straw.field(permission_classes=[scheme.AlwaysFailPermission])
    def always_fail(self) -> ty.Optional[str]:
        return "Hey"

    @straw.field
    async def error(self, message: str) -> ty.AsyncGenerator[str, None]:
        yield GraphQLError(message)  # type: ignore

    @straw.field
    async def exception(self, message: str) -> str:
        raise ValueError(message)

    @straw.field
    def teapot(self, info: Info[ty.Any, None]) -> str:
        info.context["response"].status_code = 418

        return "I'm A TEAPOT!!! 🫖"

    @straw.field
    def root_name(self) -> str:
        return type(self).__name__

    @straw.field
    def value_from_context(self, info: Info[ty.Any, ty.Any]) -> str:
        return info.context["custom_value"]

    @straw.field
    def returns_401(self, info: Info[ty.Any, ty.Any]) -> str:
        response = info.context["response"]
        if hasattr(response, "set_status"):
            response.set_status(401)
        else:
            response.status_code = 401

        return "hey"

    @straw.field
    def set_header(self, info: Info[ty.Any, ty.Any], name: str) -> str:
        response = info.context["response"]
        response.headers["X-defs.Name"] = name

        return name
