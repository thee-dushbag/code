import click
import rich

from ._hi import NAME_KEY, hi

HI_FORMAT = (
    "[green]Hello [yellow][italic]{name}[/yellow][/italic][green], how was your day?"
)


@click.group
def app():
    "Greet people."


def _show_error(error: Exception, fmt):
    try:
        rich.print(
            f"[red bold]ERROR: [white]Invalid format string. [yellow underline italic]'{fmt}'"
        )
        rich.print(f"[blue]Info: [red underline]{repr(error)!r}")
    except Exception:
        click.echo(f"ERROR: Invalid format string. '{fmt}'")
        click.echo(f"Info: {repr(error)!r}")


def _test_format(fmt: str, key: str = NAME_KEY):
    data = {key: "value"}
    try:
        _ = fmt.format(**data)
    except Exception as e:
        _show_error(e, fmt)
        exit(1)


def _say_hi(rich_fmt: str):
    try:
        rich.print(rich_fmt)
    except Exception as e:
        _show_error(e, rich_fmt)
        exit(1)


@app.command()
@click.option("-f", "--format", type=str, default=HI_FORMAT)
@click.option("-k", "--key", type=str, default=NAME_KEY)
@click.argument("name", type=str)
def greet(format: str, name: str, key: str):
    f"""Greet a given name with some format.
    default: format '{HI_FORMAT}'
    default: key '{NAME_KEY}'
    """
    _test_format(format, key)
    _say_hi(hi(name, format=format, key=key))


if __name__ == "__main__":
    app()
