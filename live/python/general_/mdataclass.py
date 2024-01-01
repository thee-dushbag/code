class Person:
    def __init__(self, name: str, email: str, age: int):
        self.name = name
        self.age = age
        self.email = email


class Auth:
    def __init__(self, username: str, password: str) -> None:
        self.password = password
        self.username = username


def dataclass(cls: type) -> type:
    hints = cls.__annotations__
    from inspect import Parameter, Signature
    sig = Signature(
        [
            Parameter(name, Parameter.POSITIONAL_OR_KEYWORD, annotation=ptype)
            for name, ptype in hints
        ]
    )

    class MyClass(cls):
        def __init__(self, *args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            for name, value in bound.arguments:
                setattr(self, name, value)

        def __eq__(self, o):
            for argname in hints.keys():
                print(f"Cheking: {argname}")
                if getattr(self, argname) != getattr(o, argname):
                    return False
            return True

    return MyClass


@dataclass
class mPerson:
    name: str
    age: int
    email: str


@dataclass
class mAuth:
    password: str
    username: str


auth = Auth(password="mypasswd", username="myname")
mauth = mAuth(password="mypasswd", username="myname")

person = Person(name="Simon", email="simon@gmail.com", age=21)
mperson = mPerson(name="Simon", email="simon@gmail.com", age=21)

assert mauth == auth
assert mperson == person
