from contextlib import ContextDecorator, _RedirectStream
from io import StringIO


class redirect_input(_RedirectStream):
    _stream = "stdin"


class Resource(ContextDecorator):
    def __init__(self, resource: str) -> None:
        self.resource = resource

    def __enter__(self):
        print("Acquired:", self.resource)

    def __exit__(self, *_):
        print("Released:", self.resource)


internet = Resource("WIFI")
connection = Resource("CONNECTION")


@internet
@connection
def login(name: str, url: str):
    print(f"Connected to {url!r}")
    print(f"Logging in as {name!r}")


# login("MikeKeehl", "http://github.com/mikekeehl")

input_src = StringIO("Mike Shaul\nhttps://www.google.com\n")

with redirect_input(input_src):
    name = input("Name:")
    url = input("Url:")

login(name, url)
