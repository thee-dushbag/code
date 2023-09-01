from faker import Faker
import strawberry as straw, enum, typing as ty
from strawberry.file_uploads import Upload

fake = Faker()
NAME = "Stranger"

@straw.interface
class Named:
    name: str

    @classmethod
    async def resolve_type(cls, type) -> bool:
        print(f"Resolving: {type}")
        return True

@straw.enum
class Gender(enum.StrEnum):
    F = enum.auto()
    M = enum.auto()

@straw.enum
class Flavor(enum.StrEnum):
    VANILLA = "vanilla"
    STRAWBERRY = "strawberry"
    CHOCOLATE = "chocolate"

@straw.enum
class NamedEnum(enum.StrEnum):
    PERSON = enum.auto()
    COMPANY = enum.auto()

@straw.input
class FolderInput:
    files: ty.List[Upload]

@straw.input
class GreetBundle:
    name: str
    template: ty.Optional[str] = None
