from pathlib import Path
import click
import json
import yaml
import tomllib as toml


@click.group()
@click.option("+d/-d", "debug", default=False, help="Turn on/off debug mode.")
@click.pass_context
def cli(ctx: click.Context, debug: bool):
    click.echo("Debug mode is %s." % ("on" if debug else "off"))
    ctx.obj = {"debug": debug}


@cli.command()
@click.pass_context
def sync(ctx: click.Context):
    click.echo("Syncing")
    ctx.invoke(add, a=12, b=13)
    if ctx.obj["debug"]:
        click.echo("Debug in sync.")


@cli.command(short_help="Greet a person given their name")
@click.option("--name", type=str, default="stranger")
def sayhi(name: str):
    "This command does the unthinkable, greet a person given their name. Huh? Genius."
    click.echo("Hello %s, how was your day?" % name.title())


@cli.command()
@click.option("-a", default=0, type=int)
@click.option("-b", default=0, type=int)
@click.pass_context
def add(ctx: click.Context, a: int, b: int):
    if ctx.obj["debug"]:
        click.echo(f"Adding {a} to {b}.")
    click.echo(f"{a} + {b} = {a + b}")


@cli.command()
@click.option("--name", prompt=True, confirmation_prompt=True)
@click.option("--age", type=int, prompt=True)
def greet(name: str, age: int):
    """Greet a person with the name and provided age."""
    click.echo("Hello %s, you are %r years old." % (name, age))


@cli.command()
@click.pass_context
def hello(ctx: click.Context):
    """Collect name and age for person to be
    greeted and confirm before greeting the person"""
    name = click.prompt(
        "Name to greet", type=str, show_default=True, default="stranger"
    ).title()
    age = click.prompt(
        "Age of target", type=click.IntRange(min=18, max=100, clamp=False)
    )
    if click.confirm("Greet person with name %r and age %r." % (name, age)):
        ctx.invoke(greet, name=name, age=age)


@cli.command(short_help="Example code in doc help message")
def helpdoc():
    """
    This help message contains some code in it.
\b\n
    def hello(name: str) -> None:\n
        print("Hello %s, how was your day?" % name.title())\n
\b
    The above function takes in a name and greets the person
    identified with it.
    """

def load_config(file: Path, loader) -> dict:
    config = {}
    try:
        # click.echo("Loading config from %s" % file.relative_to(Path.cwd()))
        config_text = file.read_text()
        # click.echo("Parsing configuration. %r" % config_text)
        config = loader(config_text)
    except FileNotFoundError:
        pass # click.echo("Config file not found.", err=True)
    except json.JSONDecodeError:
        pass # click.echo("Malformed config text, JSONDecodeError.")
    except yaml.YAMLError:
        pass # click.echo("Malformed config text, YAMLError.")
    except toml.TOMLDecodeError:
        pass # click.echo("Malformed config text, TOMLDecodeError.")

    for person in []: # config.get("people", []):
        print(person)

    return config


CONFIG_PATH = Path.cwd() / "config.toml"
CONFIG_PATH = Path.cwd() / "config.json"
CONFIG_PATH = Path.cwd() / "config.yaml"

if __name__ == "__main__":
    cli.invoke_without_command = True
    cli(default_map=load_config(CONFIG_PATH, yaml.safe_load))
