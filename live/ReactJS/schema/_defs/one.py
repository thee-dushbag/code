import strawberry as straw
from .globals import fake


@straw.type
class Company:
    name: str
    email: str

    def is_type_of(self, interface) -> bool:
        print("Is_Type_Of function Called for COMPANY")
        return True

    @classmethod
    async def create(cls):
        name = fake.company()
        email = fake.company_email()
        return cls(name=name, email=email)


@straw.type
class Person:
    name: str
    age: int

    def is_type_of(self, interface) -> bool:
        print("Is_Type_Of function Called for PERSON")
        return True

    @classmethod
    async def create(cls):
        name = fake.name()
        age = fake.random_int(10, 70)
        return cls(name=name, age=age)


@straw.type
class Name:
    fullname: str

    @straw.field
    def first_name(self) -> str:
        name, _, _ = self.fullname.partition(" ")
        return name

    @straw.field
    def last_name(self) -> str:
        _, _, name = self.fullname.rpartition(" ")
        return name
