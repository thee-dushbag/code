from dataclasses import dataclass
from pathlib import Path
import click


@click.group
def app():
    ...


@app.command("init")
def init_db():
    click.echo("Initializing the database.")


@click.command("del")
@click.confirmation_option()
def delete_db():
    click.echo("Dropping the database.")


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
#     "--password", "-p", type=str, prompt=True, confirmation_prompt=True, hide_input=True
# )
@click.password_option("--password", "-p")
def signup(name: str, password: str):
    if name in _users:
        return print("Username already taken!!!")
    print("Signup was Successful!")


if __name__ == "__main__":
    app.add_command(delete_db)
    app()
