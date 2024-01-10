"Chain of responsibility design pattern"

import typing, re, rich

validname = re.compile("^[a-z]+ [a-z]+$", re.I)


class Error(Exception):
    def __init__(self, type: str, message: str) -> None:
        self.type = type
        self.message = message

    def __str__(self):
        return f"[{self.type}] Error: {self.message}"


class Request(dict[str, object]):
    ...


class Handler(typing.Protocol):
    def handle(self, request: Request) -> object:
        ...


def greet(name: str):
    return f"Hello {name}, how was your day?"


def confirmvoter(age: int):
    return f"{age} is allowed to vote!"


class Age:
    def __init__(self, next) -> None:
        self.next = next

    def handle(self, request: Request):
        sentinel = object()
        age = request.get("age", sentinel)
        if age is sentinel:
            raise Error("missing field", "expected a integer field age.")
        if not isinstance(age, int):
            raise Error("type error", f"expected integer age, got {type(age).__name__}")
        if age < 18:
            raise Error("underage", "too young for this.")
        if age >= 100:
            raise Error("overage", "too old for this.")
        return self.next.handle(request)


class Name:
    def __init__(self, next) -> None:
        self.next = next

    def handle(self, request: Request):
        sentinel = object()
        name = request.get("name", sentinel)
        if name is sentinel:
            raise Error("missing field", "expected a string field name.")
        if not isinstance(name, str):
            raise Error(
                "type error", f"expected string name, got {type(name).__name__}"
            )
        if re.match(validname, name) is None:
            raise Error(
                "invalid name",
                f"expected an alphabetic space separated first and last name, got {name!r}",
            )
        return self.next.handle(request)


class GreetPatVoterHandler:
    def handle(self, request: Request):
        name: str = typing.cast(str, request["name"])
        age: int = typing.cast(int, request["age"])
        return " ".join([greet(name), confirmvoter(age)])


class Application:
    def __init__(self, base: Handler) -> None:
        self.base = base

    def make_request(self, request):
        try:
            return dict(
                status="okay", result=self.base.handle(request), request=request
            )
        except Error as e:
            return dict(status="error", result=str(e), request=request)


greetvoter = GreetPatVoterHandler() # Core of the application
name = Name(greetvoter) # Name validator
age = Age(name) # Age validator
app = Application(age) # Entry point to our application

requests = [
    Request(age=38),
    Request(name="Faith Njeri"),
    Request(name="Simon", age=21),
    Request(name="Simon 1234", age=21),
    Request(name="Faith Njeri", age=15),
    Request(name="Simon Nganga@", age=21),
    Request(name="Lydia Njeri", age="38"),
    Request(name=b"Simon Nganga", age=21),
    Request(name="Babu Nganga", age=100),
    Request(name="Simon Nganga", age=21),
]

#   <-----------------------------------------------------
#                                                        |
# request -> app -> age_validator -> name_validator -> greeter

for response in map(app.make_request, requests):
    rich.print(response)
