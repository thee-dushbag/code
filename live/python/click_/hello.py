import click, string, typing, multiprocessing as mt

KEY = "name"
TEMPLATE = f"Hello ${KEY}, how was your day?"


@click.command
@click.argument("names", nargs=-1)
@click.option("--key", default=KEY)
@click.option("--style/--no-style", default=True)
@click.option("--template", "-t", default=TEMPLATE)
def hello(names: typing.Iterable[str], template: str, key: str, style: str) -> None:
    if style:
        names = map(str.title, names)
    try:
        _template = string.Template(template)
        for name in names:
            click.echo(_template.substitute(**{key: name}))
    except KeyError as e:
        click.echo(f"Unknown entry in template: {e!s}", err=True)
        exit(1)


if __name__ == "__main__":
    hello()
