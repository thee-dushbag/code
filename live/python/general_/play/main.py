import enum

from attrs import converters as c
from attrs import define, field
from attrs import validators as v

EMAIL_RE = r"(?P<username>\w+)@(?P<provider>\w+)\.(?P<domain>\w+)"


class Gender(enum.StrEnum):
    MALE = enum.auto()
    FEMALE = enum.auto()


def g(value):
    if not isinstance(value, Gender):
        return Gender(str(value).lower())
    return value


@define
class Person:
    name: str
    email: str
    gender: Gender = field(converter=g)

    @gender.validator
    def _(self, attr, value):
        val1 = v.in_([Gender.MALE, Gender.FEMALE])
        val1(self, attr, value)


me = Person("Simon", "simon9@gmail.com", "MALe")
print(me)
