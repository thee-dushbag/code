import typing as t
from typing import Any

import click
from click.core import Context, Parameter
from mpack.number_reader import get_reader

reader = get_reader("english")


class MyType(click.ParamType):
    name = "mytype"

    def convert(self, value: Any, param: Parameter | None, ctx: Context | None) -> Any:
        return f"MyType({value!r})"


@click.group()
def cli():
    "I am Learning click python package."


@click.command()
def hello_world():
    click.echo("Hello World from click.")


@cli.command()
def sayhi():
    click.echo("Hello, how are you?")


@cli.command()
@click.option("--count", "-c", default=5, help="Count to a given number: count")
def count_to(count: int):
    for i in range(1, count + 1):
        click.echo(f"Counting at: {i}")


@cli.command()
@click.argument("name")
def say_hi(name: str):
    click.echo(f"Hello {name}, how was your day?")


MYTYPE = MyType()


@cli.command()
@click.option("--name", default="Simon Nganga", type=MYTYPE)
@click.argument("value", type=MYTYPE)
def mytype(name, value: str):
    click.echo(f"Received: {name=!r}, {value=!r}")


@cli.command()
@click.option("--position", default=(500, 500), nargs=2, type=int)
def move_to(position: tuple[int, int]):
    import pyautogui as pg

    pg.click(*position)
    pg.write("Hello World")


class NameAge(click.ParamType):
    name = "nameage"

    def convert(self, value: str, parameter, ctx) -> tuple[str, int]:
        name, _, sage = value.partition(" ")
        try:
            if len(name) < 3 or not name.isalpha():
                raise Exception(f"Invalid Name: {name!r}")
            name = name.title()
            age = int(sage)
            return name, age
        except Exception as e:
            self.fail(str(e), parameter, ctx)


NAME_AGE = NameAge()


@cli.command()
@click.argument("nameage", type=NAME_AGE)
def nameage(nameage: tuple[str, int]):
    name, age = nameage
    print(f"Hello {name}, how was your day?")
    print(f"You are {age} years old.")
    print(f"You will be 60 years old in {60 - age} years to come.")


@cli.command()
@click.argument("name", type=str)
@click.argument("age", type=int)
def nameagetwo(name: str, age: int):
    print(f"Hello {name}, how was your day?")
    print(f"You are {age} years old.")
    print(f"You will be 60 years old in {60 - age} years to come.")


@cli.command()
@click.option("--message", "-m", multiple=True, type=str)
def messages(message: list[str]):
    for index, msg in enumerate(message, start=1):
        print(f"Message {reader(index)}: {msg!r}")


if __name__ == "__main__":
    cli.add_command(hello_world)
    cli()
