import asyncio as aio
import base64
import typing as ty

import schema._defs as defs
import strawberry as straw

# from ._trash import Query as QueryOne


@straw.type
class Query:
    @straw.field
    async def greet(
        self, name: ty.Optional[str] = None, template: ty.Optional[str] = None
    ) -> defs.Greeting:
        name = name if name is not None else defs.NAME
        return defs.Greeting(name=name, template=template)

    @straw.field
    async def greet_bundle(self, bundle: defs.GreetBundle) -> defs.Greeting:
        return defs.Greeting(name=bundle.name, template=bundle.template)

    @straw.field
    async def fake(self, field: str) -> str:
        method = getattr(defs.fake, field, lambda: "")
        resp = method()
        if isinstance(resp, bytes):
            return base64.b64decode(resp).decode()
        return str(resp)

    @straw.field
    async def profile(self) -> defs.Profile:
        profile = defs.fake.profile()
        profile["current_location"] = defs.fake.address()
        profile["sex"] = profile["sex"].lower()
        profile["name"] = defs.Name(fullname=profile["name"])
        # profile['image'] = defs.fake.image()
        return defs.Profile(**profile)
