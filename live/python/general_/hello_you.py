
GREETING_TEMPLATE: str = "Hello %s, how was your day?"

def hello(name: str, template: None | str = None) -> str:
    return (GREETING_TEMPLATE if template is None else template) % name

class Greeter:
    def __init__(self, template: str | None = None) -> None:
        self.template = GREETING_TEMPLATE if template is None else template

    def greet(self, name: str) -> str:
        return hello(name, self.template)

def get_template(envname: str | None = None) -> str | None:
    from os import getenv
    return getenv(envname or "GREETING_TEMPLATE")

def main(names: list[str]):
    greeter = Greeter(get_template("GREETER"))
    for name in names:
        greeting = greeter.greet(name)
        print(greeting)

if __name__ == "__main__":
    from sys import argv
    main(argv[1:])

