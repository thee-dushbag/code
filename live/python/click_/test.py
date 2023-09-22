from pathlib import Path
from string import Template

import click


@click.group
def cli():
    "Learning click Library..."


TEMPLATE = Template("Hello $name, how was your day?")


class TemplateParam(click.ParamType):
    def convert(self, value: str | Template, param, ctx) -> Template:
        if isinstance(value, Template):
            return value
        return Template(value)


@cli.command
@click.argument("name")
@click.option(
    "--template",
    "-t",
    type=TemplateParam(),
    help="Greeting template for greeting person.",
    default=TEMPLATE,
)
def hello(name: str, template: Template):
    greeting = template.substitute(name=name)
    click.echo(greeting)


@cli.command
@click.argument("text")
@click.option("--editor", "-e", default="/usr/bin/nvim")
def edit(text: str, editor: str):
    ntext = click.edit(text, editor=editor)
    click.echo(f"New Text: {ntext if ntext is not None else '<content lost>'}")


@cli.command
@click.option("--user", "-u", prompt=True)
@click.password_option()
def login(password: str, user: str):
    click.echo(f"Signing in as {user!r} with {password = !r}")


@cli.command
@click.argument("file", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.confirmation_option()
def delete(file: click.File):
    click.echo(f"Deleting file {file!r}...")
    Path(str(file)).unlink()


@cli.command
@click.option("--name", type=click.STRING, prompt=True)
@click.option("--age", type=click.INT, prompt=True)
@click.option("--email", type=click.STRING, prompt=True)
@click.option("--school", type=click.STRING, prompt=True)
def signup(name: str, age: int, email: str, school: str):
    click.echo(f"+-------+------------[ PERSON ]----+")
    click.echo(f"| Name  | {name}")
    click.echo(f"| School| {school}")
    click.echo(f"| Email | {email}")
    click.echo(f"| Age   | {age}")
    click.echo(f"+-------+--------------------------+")


if __name__ == "__main__":
    cli()
