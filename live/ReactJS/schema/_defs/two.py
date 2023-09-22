import asyncio as aio
import time as ti
import typing as ty
from string import Template

import strawberry as straw

from .globals import TEMPLATE, Gender
from .one import Name


@straw.type
class Profile:
    job: str
    company: str
    ssn: str
    residence: str
    blood_group: str
    website: ty.List[str]
    username: str
    name: Name
    sex: Gender
    address: str
    mail: str
    current_location: str
    birthdate: str

    @straw.field
    async def shout(self, message: str, delay: ty.Optional[float] = None) -> str:
        delay = 1 if delay is None else delay
        await aio.sleep(delay)
        return message.upper() + f"!!! You are {self.name.fullname}"


@straw.type
class Greeting:
    name: ty.Annotated[str, "Name to Greet."]
    # template: ty.Optional[str] = None
    template: ty.Annotated[
        ty.Optional[str],
        "Template of the form 'Hello $name' where $name will be replaced with the name passed.",
    ] = None

    def __post_init__(self):
        self.template = TEMPLATE if self.template is None else self.template

    @property
    def temp(self) -> str:
        return ty.cast(str, self.template)

    @straw.field
    async def greeting(self) -> str:
        return Template(self.temp).substitute(name=self.name)

    @straw.field
    async def time(self) -> str:
        return ti.asctime(ti.localtime(ti.time()))
