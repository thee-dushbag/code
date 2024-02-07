from contextlib import ExitStack, closing


class Context:
    marker: str = " "
    indent_level: int = 0

    def __init__(self, id: str) -> None:
        self.identity = id

    @classmethod
    def bump_level(cls, value: int = 0, /):
        cls.indent_level += value

    def __enter__(self) -> "Context":
        print("%r {" % self.identity)
        # print(f"Entering: {self.identity}")
        self.bump_level(1)
        return self

    def __exit__(self, *_):
        self.bump_level(-1)
        # print(f"Exiting: {self.identity}")
        print("}")

    @classmethod
    def indent(cls) -> str:
        return cls.marker * cls.indent_level


def print(*args, sep=" ", end="\n"):
    string = Context.indent() + sep.join(map(str, args))
    __builtins__.print(string, sep="", end=end)


def main():
    one = Context("one")
    two = Context("two")
    three = Context("three")
    four = Context("four")

    exit = ExitStack()
    exit.enter_context(one)
    with exit:
        exit.enter_context(two)
        exit.enter_context(three)
        print("Ola")

    exit.enter_context(four)
    with closing(exit):
        exit.enter_context(two)
        work = "Something to do before closing."
        exit.callback(print, work)
        print("Last One")
        work = "Another piece of work!!!"
        exit.callback(print, work)


if __name__ == "__main__":
    Context.marker = "   "
    main()
