from pathlib import Path
import typing as ty
from pprint import pprint
import more_itertools as mt
import random as rand
from faker import Faker

fake = Faker()

T = ty.TypeVar("T")
Buffer = bytes | bytearray | memoryview


def _to_bits(
    data: Buffer, to_bit: ty.Callable[[int], str]
) -> ty.Generator[str, None, None]:
    for byte in data:
        yield to_bit(byte)


def to_bits(data: Buffer):
    return _to_bits(data, lambda b: bin(b)[2:].rjust(8, "0"))


def to_hex(data: Buffer):
    return _to_bits(data, lambda b: hex(b)[2:].rjust(2, "0"))


def to_int(data: Buffer):
    return _to_bits(data, lambda b: str(b).rjust(3, "0"))


def print_bits(
    data: Buffer,
    *,
    sep: str | None = None,
    chunk: int | None = None,
    convertor: ty.Callable[[Buffer], ty.Generator[str, None, None]] | None = None,
):
    convertor = to_bits if convertor is None else convertor
    chunk = 4 if chunk is None else chunk
    sep = " " if sep is None else sep
    grouped = mt.grouper(convertor(data), chunk, fillvalue="")
    bits = "\n".join(sep.join(chunk) for chunk in grouped)
    print(bits)


def _to_number_system(number: int, base: int):
    while True:
        number, rem = divmod(number, base)
        yield rem
        if number == 0:
            break


def _from_number_system(numbers: ty.Iterable[int], base: int):
    return sum(base**p * q for p, q in enumerate(numbers))


def to_256(number: int):
    return _to_number_system(number, 256)


def from_256(numbers: ty.Iterable[int]):
    return _from_number_system(numbers, 256)


# big_number = 986597654765432345678976543345678765434665434567876543456787654345678765434567780009876543456787654567876543236787654387654345678
# base256 = list(to_256(big_number))
# base16 = list(_to_number_system(big_number, 16))
# base10 = list(_to_number_system(big_number, 10))
# base2 = list(_to_number_system(big_number, 2))
# number = int.from_bytes(bytes(reversed(base256)))
# number = from_256(base256)

# buffer = "".join(bin(b)[2:] for b in base256)
# bits = bin(big_number)[2:]

# print(buffer)
# print(bits)

# print(f"2  : {base2}")
# print(f"10 : {base10}")
# print(f"16 : {base16}")
# print(f"256: {base256}")
# print(f"10 : {number}")
# print(f'Okay: {number == big_number}')

# print_bits(bytes(base256), convertor=to_hex)


def main():
    path = Path.cwd() / "ignore.sh"

    with path.open("rb") as file:
        number = int.from_bytes(file.read())
        # print_bits(file.read(), chunk=15, convertor=to_int)
    # print(number)
    with open("comp.bin", "wb") as file:
        file.write(bytes(to_256(number)))
    # print(path.stat().st_size)


class Value(ty.Generic[T]):
    def __init__(self, value: T) -> None:
        self.value_type: type[T] = type(value)
        self.value: T = value


providers = ["gmail", "yahoo", "outlook", "thunderbird"]
dotnet = ["com", "mil", "xyz", "org"]
domain = lambda: f"{rand.choice(providers)}.{rand.choice(dotnet)}"
_raw_email = lambda user, domain: f"{user}@{domain}"
_clean_user = lambda user: user.replace(" ", "").lower()
email = lambda user, dom=None: _raw_email(
    _clean_user(user), domain() if dom is None else dom
)

CLEAN = True


class Meta(type):
    def __new__(cls, name, bases, kwargs: dict, *, text=None, info=False):
        if info and not CLEAN:
            print("Info:", name, bases, kwargs)
            print("Text:", text)
        init = kwargs.get("__init__", lambda: None)
        kwargs["__init__"] = cls._cls_init(init)
        klass = type.__new__(cls, name, bases, kwargs)
        return klass

    @classmethod
    def _cls_init(cls, original):
        def wrap_init(self, *args, **kwargs):
            klass = type(self)
            print("__init__:", klass, args, kwargs)
            cls.instances.setdefault(klass, set()).add(self)
            return original(self, *args, **kwargs)

        return wrap_init

    instances = {}

    def get_instances(self):
        return self.instances[self]


class Person(metaclass=Meta, text="From Person", info=True):
    def __init__(self, name: str, age: int) -> None:
        self._domain: str = domain()
        self.name = name
        self.age = age
        print("PERSON_INIT:", self)

    @property
    def email(self) -> str:
        return email(self.name, self._domain)

    @property
    def voter(self) -> bool:
        return self.age >= 18

    def _properties(self):
        return dict(
            cls_name=self.__class__.__name__,
            self_id_hex=hex(id(self)),
            cls=self.__class__,
            self_id=id(self),
            email=self.email,
            voter=self.voter,
            name=self.name,
            age=self.age,
        )

    def __format__(self, __format_spec: str) -> str:
        return __format_spec % self._properties()

    def __str__(self) -> str:
        return format(
            self,
            "%(cls_name)s(name=%(name)r, age=%(age)s, email=%(email)r, voter=%(voter)s)",
        )

    def __repr__(self) -> str:
        return format(
            self,
            "<object %(cls_name)s at %(self_id_hex)s with "
            "(name=%(name)r, age=%(age)s, email=%(email)r)>",
        )


class Employee(Person, text="From Employee", info=True):
    def __init__(self, name: str, age: int, job: str) -> None:
        self.job = job
        super().__init__(name, age)

    def _properties(self):
        return dict(**super()._properties(), job=self.job)

    def __str__(self) -> str:
        return format(
            self,
            "%(cls_name)s(name=%(name)r, age=%(age)s, job="
            "%(job)r, email=%(email)r, voter=%(voter)s)",
        )

    def __repr__(self) -> str:
        return format(
            self,
            "<object %(cls_name)s at %(self_id_hex)s with "
            "(name=%(name)r, age=%(age)s, job=%(job)r)>",
        )


class PersonDetails(ty.TypedDict):
    name: str
    age: int


class EmployeeDetails(PersonDetails):
    job: str


def _person_details() -> PersonDetails:
    return PersonDetails(name=fake.name(), age=fake.random.randint(10, 70))


def _employee_details() -> EmployeeDetails:
    return EmployeeDetails(**_person_details(), job=fake.job())


def create_person() -> Person:
    return Person(**_person_details())


def create_employee() -> Employee:
    return Employee(**_employee_details())


class mA(type):
    def __new__(cls, name, bases, kwargs, *, ma):
        cls.ma = ma
        return super().__new__(cls, name, bases, kwargs)

    def __getattribute__(self, __name: str) -> ty.Any:
        print("mA.__getattribute__:", __name)
        return super().__getattribute__(__name)

    def m_A(self):
        print("mA.m_A()")


class mB(mA):
    def __new__(cls, name, bases, kwargs, *, mb):
        cls.mb = mb
        return super().__new__(cls, name, bases, kwargs, ma="MA")

    def __getattribute__(self, __name: str) -> ty.Any:
        print("mB.__getattribute__:", __name)
        return super().__getattribute__(__name)

    def m_B(self):
        print("mB.m_B()")


class mC(mB):
    def __new__(cls, name, bases, kwargs, *, mc):
        cls.mc = mc
        return super().__new__(cls, name, bases, kwargs, mb="MB")

    def __getattribute__(self, __name: str) -> ty.Any:
        print("mC.__getattribute__:", __name)
        return super().__getattribute__(__name)

    def m_C(self):
        print("mC.m_C()")


class A(object, metaclass=mA, ma="MA"):
    def __init__(self, a) -> None:
        self.a = a

    def __getattribute__(self, __name: str) -> ty.Any:
        print("A.__getattribute__:", __name)
        return super().__getattribute__(__name)

    def m_a(self):
        print("A.m_a()")

    def cls_attr(self):
        print(__class__.ma)


class B(A, metaclass=mB, mb="MB"):
    def __init__(self, b) -> None:
        super().__init__("a")
        self.b = b

    def __getattribute__(self, __name: str) -> ty.Any:
        print("B.__getattribute__:", __name)
        return super().__getattribute__(__name)

    def m_b(self):
        print("B.m_b()")

    def cls_attr(self):
        print(__class__.mb)


class C(B, metaclass=mC, mc="MC"):
    def __init__(self, c) -> None:
        super().__init__("b")
        self.c = c

    def __getattribute__(self, __name: str) -> ty.Any:
        print("C.__getattribute__:", __name)
        return super().__getattribute__(__name)

    def m_c(self):
        print("C.m_c()")

    def cls_attr(self):
        print(__class__.mc)

def inheritance():
    i = C("c")
    print(i, type(i))
    print(type(i), type(type(i)))
    print(type(type(i)), type(type(type(i))))
    print(type(type(type(i))), type(type(type(type(i)))))
    return
    print(C.ma)
    print(C.mb)
    print(C.mc)
    A.ma
    B.mb
    C.mc
    A.m_A()
    B.m_B()
    C.m_C()
    i = C("c")
    i.a
    i.b
    i.c
    i.m_c()
    i.m_b()
    i.m_a()


def test_match():
    # employees = [create_employee() for _ in range(2)]
    # people = [create_person() for _ in range(3)]
    # print(employees)
    # print(people)
    # everyone = [*employees, *people]
    # rand.shuffle(everyone)
    # print(everyone)
    sis = Person("Faith", 11)
    me = Employee("Simon", 21, "Software engineer")
    match me:
        case Person(name=name, age=age, email=email):
            print(f"My name is {name} and I am {age} years old.")
            print(f"Contact me via {email}")
        case Person(voter=True):
            print("I can vote.")
        case Person(voter=False):
            print("I cannot vote.")
    pprint(Meta.instances)
    print(Employee.get_instances())
    print(Employee.__class__)
    print(me.__class__)
    # print(me.get_instances())


def hello():
    match = 89
    # match <expression>:
    #     case result1: <handle if expression evalueates to result1>
    #     case result2: <handle if expression evalueates to result2>
    #     ...
    #     case resultn: <handle if expression evalueates to resultn>
    #     case <capture_name>: # capture_name is now a variable holding the actual
    #         # result of the expression, you can use it in the block of this case
    #         <handle if none of the cases above equal the result>
    match match:
        case 89:
            print("found: 89")
        case found:
            print("not found:", found)

    v = Value(90)
    match v:
        case Value(value_type=vtype) as V:
            print("Not arg:", vtype, V.value)
        case Value(value=value) as V:
            print(V.value_type, value)
        case Value(value=value):
            print("found a %r" % value)
        case value if value.value_type is int:
            print("found a Value[int]")
        case value if value.value_type is str:
            print("found a Value[str]")

    base = bytes([255, 255])
    base = list(to_256(256 * 256))
    print("base256:", base)
    print("base10:", from_256(base))


if __name__ == "__main__":
    # test_match()
    inheritance()
