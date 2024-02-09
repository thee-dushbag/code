from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO
import click


def print_version(ctx: click.Context, param: click.Parameter, value: bool):
    if not value or ctx.resilient_parsing:
        return
    click.echo("Version 1.23:5f")
    ctx.exit()


@click.group(invoke_without_command=True)
@click.option(
    "-V",
    "--version",
    is_flag=True,
    default=False,
    is_eager=True,
    expose_value=False,
    callback=print_version,
    help="Show application version",
)
def app():
    "Learning Click!!!"


@app.command("init")
def init_db():
    click.echo("Initializing the database.")


def abort_if_false(ctx: click.Context, param: click.Parameter, value: bool):
    if not value:
        ctx.abort()


@click.command("del")
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt="Are you sure?",
    help="Confirm deletion of database.",
)
# @click.confirmation_option("--yes", "-y")
def delete_db():
    from time import sleep
    from random import random

    with click.progressbar(range(100), color=True, label="Dropping") as bar:
        for _ in bar:
            sleep(random() / 4)


@app.command
@click.option(
    "-w",
    "--word",
    envvar="MAGIC_WORD",  # Environment variable to get the value from if not passed on cmd
    type=str,
    default="",
)
def magic_word(word: str):
    if word.lower() in ("please", "excuse", "thanks"):
        return print("Congratulations, you passed!!!")
    print("Try again, hint: be more polite!")


class Names(click.types.StringParamType):
    envvar_list_splitter: str = ","
    # def split_envvar_value(self, names: str) -> Sequence[str]:
    #     return names.split(",")


title = lambda _, __, names: map(str.lower, names)
greet = lambda name: f"Hello {name}, how was your day?"


@app.command
@click.option(
    "--names", "-n", multiple=True, callback=title, type=Names(), envvar="GREET_NAMES"
)
def greet_all(names: list[str]):
    for name in names:
        print(greet(name))


@app.command
@click.argument("sources", nargs=-1, type=click.File("rb"))  # Variadic arguments
@click.argument("destination", type=click.File("wb"))
@click.option(
    "--chunk", "-s", "chunk_size", type=click.IntRange(64, 2**31, clamp=True)
)
def stream_to(sources: list[BinaryIO], destination: BinaryIO, chunk_size: int):
    for source in sources:
        while chunk := source.read(chunk_size):
            destination.write(chunk)


@app.command
@click.option("--bool", "-b", type=click.BOOL)
@click.option("--str", "-s", type=click.STRING)
@click.option("--int", "-i", type=click.INT)
@click.option("--float", "-f", type=click.FLOAT)
@click.option("--uuid", "-u", type=click.UUID)
def ptypes(**types):
    for name, value in types.items():
        click.echo("%s: %r" % (name, value))


@app.command("read")
@click.argument("file", type=click.File())
def read_file(file):
    click.echo(file.read())


@app.command("inspect")
@click.argument(
    "path",
    type=click.Path(exists=True, resolve_path=False, readable=False, path_type=Path),
)
def inspect_path(path: Path):
    click.echo("path:             %s" % path)
    click.echo("is_regular_file:  %r" % path.is_file())
    click.echo("is_directory:     %r" % path.is_dir())
    click.echo("absolute:         %s" % path.resolve())
    click.echo("path_uri:         %r" % path.absolute().as_uri())
    click.echo("resolved_uri:     %r" % path.absolute().resolve().as_uri())


@app.command("register")
@click.option(
    "--gender",
    "-g",
    prompt=True,
    type=click.Choice(["male", "female"]),
    callback=lambda c, p, v: v.lower(),
)
@click.option("--age", "-a", prompt=True, type=click.IntRange(18, 70))
@click.option("--skin", "-s", prompt=True, type=click.Choice(["black", "white", "red"]))
@click.option("--name", "-n", prompt=True, type=str)
def reg(name, skin, gender, age):
    click.echo("Registered a %s year old %s %s called %s." % (age, skin, gender, name))


@dataclass
class Name:
    first: str
    last: str


class FirstLastName(click.ParamType):
    name = "Name"

    def convert(
        self, value: str, param: click.Parameter | None, ctx: click.Context | None
    ) -> Name:
        if value.count(" ") == 1:
            first, last = value.split(" ")
        else:
            raise click.BadParameter(
                f'Expected a name of format "<first> <second>", got {value!r}.',
                ctx,
                param,
            )
        return Name(first, last)


@app.command("names")
@click.argument("target", type=FirstLastName())
def your_name(name: Name):
    click.echo(f"Your names are {name.first!r} and {name.last!r}.")


Password, User = str, str
_users: dict[User, Password] = dict(
    simon="SimonNganga",
    faith="FaithNjeri",
    darius="KimaniKim",
)


@app.command
@click.option("--username", "-U", type=str, prompt=True)
@click.option("--password", "-P", type=str, prompt=True, hide_input=True)
def login(username: str, password: str):
    if passwd := _users.get(username):
        if passwd == password:
            return print("Login Successful!")
        return print("Provided password is incorrect!")
    print("No such user was found!")


@app.command
@click.option("--name", "-n", type=str, prompt=True)
# @click.option(
#    "--password",
#    "-p", type=str,
#    prompt=True,
#    confirmation_prompt=True,
#    hide_input=True)
@click.password_option("--password", "-p")
def signup(name: str, password: str):
    if name in _users:
        return print("Username already taken!!!")
    print("Signup was Successful!")


if __name__ == "__main__":
    app.add_command(delete_db)
    app()
